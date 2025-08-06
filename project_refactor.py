import os
import sys
import shutil
import ast
import re
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import print as rprint
import argparse
try:
    import networkx as nx
except ImportError:
    nx = None
try:
    import graphviz
except ImportError:
    graphviz = None

console = Console()

# ---------------------- Argument Parsing ----------------------
def parse_args():
    parser = argparse.ArgumentParser(description="ERP Project Refactor & Audit Tool")
    parser.add_argument('--dry-run', action='store_true', help='عرض التقرير بدون تغيير الملفات فعليًا')
    parser.add_argument('--auto-fix', action='store_true', help='تنفيذ كل الإصلاحات تلقائيًا')
    parser.add_argument('--interactive', action='store_true', help='تأكيد يدوي قبل حذف أو إعادة تسمية أي ملف')
    parser.add_argument('--export-graph', action='store_true', help='تصدير علاقات الملفات على شكل .dot أو .png')
    return parser.parse_args()

# ---------------------- File Discovery ----------------------
def discover_files(root):
    exts = ['.py', '.json', '.ui', '.qss', '.db', '.log', '.png', '.jpg', '.jpeg']
    files = []
    for p in Path(root).rglob('*'):
        if p.is_file() and (p.suffix.lower() in exts or p.name.startswith('.')):
            files.append(p)
    return files

# ---------------------- AST Analysis ----------------------
def analyze_py_file(file_path):
    result = {'classes': [], 'functions': [], 'main': False, 'imports': [], 'unused_imports': [], 'duplicate_defs': []}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                result['classes'].append(node.name)
            elif isinstance(node, ast.FunctionDef):
                result['functions'].append(node.name)
            elif isinstance(node, ast.If):
                if (isinstance(node.test, ast.Compare) and hasattr(node.test.left, 'id') and node.test.left.id == '__name__'):
                    result['main'] = True
            elif isinstance(node, ast.Import):
                for n in node.names:
                    result['imports'].append(n.name)
            elif isinstance(node, ast.ImportFrom):
                result['imports'].append(node.module)
        # Unused imports (simple heuristic)
        used = set(re.findall(r'\b([A-Za-z_][A-Za-z0-9_]*)\b', source))
        result['unused_imports'] = [imp for imp in result['imports'] if imp and imp not in used]
        # Duplicate defs
        result['duplicate_defs'] = [name for name in set(result['functions']) if result['functions'].count(name) > 1]
    except Exception as e:
        result['error'] = str(e)
    return result

# ---------------------- Dependency Graph ----------------------
def build_dependency_graph(py_files):
    graph = nx.DiGraph() if nx else None
    edges = []
    for f in py_files:
        info = analyze_py_file(f)
        for imp in info['imports']:
            if imp:
                edges.append((str(f), imp))
                if graph:
                    graph.add_edge(str(f), imp)
    return graph, edges

# ---------------------- Project Structure ----------------------
def create_structure(root, dry_run=False):
    structure = {
        'erp_project': ['main.py', 'requirements.txt', 'README.md', 'config.py',
            {'app': ['__init__.py', 'core/', 'database/', 'models/', 'ui/', 'views/', 'controllers/', 'utils/', 'media/', 'styles/', 'logs/']},
            'tests/'
        ]
    }
    def make_dir(path):
        if not dry_run:
            os.makedirs(path, exist_ok=True)
    def make_file(path):
        if not dry_run:
            Path(path).touch()
    base = Path(root) / 'erp_project'
    make_dir(base)
    for item in structure['erp_project']:
        if isinstance(item, str):
            if item.endswith('/'):
                make_dir(base / item)
            else:
                make_file(base / item)
        elif isinstance(item, dict):
            for k, v in item.items():
                make_dir(base / k)
                for sub in v:
                    if sub.endswith('/'):
                        make_dir(base / k / sub)
                    else:
                        make_file(base / k / sub)
    return base

# ---------------------- Quality Audit ----------------------
def code_quality_audit(files):
    stats = {'files': len(files), 'py_files': 0, 'classes': 0, 'functions': 0, 'main_points': 0, 'unused_imports': [], 'duplicate_defs': [], 'issues': []}
    for f in files:
        if f.suffix == '.py':
            stats['py_files'] += 1
            info = analyze_py_file(f)
            stats['classes'] += len(info['classes'])
            stats['functions'] += len(info['functions'])
            if info['main']:
                stats['main_points'] += 1
            stats['unused_imports'].extend(info['unused_imports'])
            stats['duplicate_defs'].extend(info['duplicate_defs'])
            if info.get('error'):
                stats['issues'].append((str(f), info['error']))
    return stats

# ---------------------- File Renaming ----------------------
def suggest_rename(file_path):
    name = file_path.name
    # Example rules
    if re.match(r'window\d+_final.py', name):
        return 'item_entry_window.py'
    if re.match(r'backup_copy\d+.py', name):
        return 'deprecated_inventory.py'
    if name == 'newmodule.py':
        return 'inventory_controller.py'
    # More rules can be added based on content
    return None

def rename_files(files, dry_run=False, interactive=False):
    renamed = []
    for f in files:
        new_name = suggest_rename(f)
        if new_name and new_name != f.name:
            if interactive:
                resp = input(f"Rename {f.name} to {new_name}? [y/N]: ")
                if resp.lower() != 'y':
                    continue
            if not dry_run:
                f.rename(f.parent / new_name)
            renamed.append((f.name, new_name))
    return renamed

# ---------------------- Advanced Cleanup ----------------------
def advanced_cleanup(root, files, dry_run=False, interactive=False):
    removed = []
    for f in files:
        if f.name == '__pycache__' or f.suffix in ['.pyc', '.log', '.bak']:
            if interactive:
                resp = input(f"Delete {f}? [y/N]: ")
                if resp.lower() != 'y':
                    continue
            if not dry_run:
                if f.is_dir():
                    shutil.rmtree(f)
                else:
                    f.unlink()
            removed.append(str(f))
    # Remove unused images, old dbs, etc. (placeholder)
    return removed

# ---------------------- Audit Report ----------------------
def generate_report(stats, renamed, removed, issues, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# تقرير تدقيق المشروع\n\n")
        f.write(f"عدد الملفات: {stats['files']}\n")
        f.write(f"ملفات بايثون: {stats['py_files']}\n")
        f.write(f"عدد الكلاسات: {stats['classes']}\n")
        f.write(f"عدد الدوال: {stats['functions']}\n")
        f.write(f"نقاط الدخول (main): {stats['main_points']}\n\n")
        f.write(f"الاستيرادات غير المستخدمة: {stats['unused_imports']}\n")
        f.write(f"الدوال المكررة: {stats['duplicate_defs']}\n")
        f.write(f"المشكلات: {issues}\n\n")
        f.write(f"الملفات التي أعيد تسميتها: {renamed}\n")
        f.write(f"الملفات التي تم حذفها: {removed}\n")
        f.write("\nاقتراحات احترافية:\n- أضف __init__.py في كل مجلد بايثون\n- تحقق من الاستيرادات الدائرية\n- أعد تسمية الملفات غير الوصفية\n- نظف الصور والملفات غير المستخدمة\n")

# ---------------------- Export Graph ----------------------
def export_graph(edges, output_path):
    if graphviz:
        dot = graphviz.Digraph()
        for src, dst in edges:
            dot.edge(src, dst)
        dot.render(output_path, format='png')
    elif nx:
        import matplotlib.pyplot as plt
        g = nx.DiGraph()
        g.add_edges_from(edges)
        nx.draw(g, with_labels=True)
        plt.savefig(output_path)
    else:
        with open(output_path + '.dot', 'w', encoding='utf-8') as f:
            for src, dst in edges:
                f.write(f'"{src}" -> "{dst}";\n')

# ---------------------- Main ----------------------
def main():
    args = parse_args()
    root = Path(os.getcwd())
    files = discover_files(root)
    py_files = [f for f in files if f.suffix == '.py']
    # تحليل AST وبناء العلاقات
    stats = code_quality_audit(files)
    graph, edges = build_dependency_graph(py_files)
    # إعادة هيكلة المشروع
    new_base = create_structure(root, dry_run=args.dry_run)
    # إعادة تسمية الملفات
    renamed = rename_files(py_files, dry_run=args.dry_run, interactive=args.interactive)
    # تنظيف متقدم
    removed = advanced_cleanup(root, files, dry_run=args.dry_run, interactive=args.interactive)
    # توليد تقرير التدقيق
    generate_report(stats, renamed, removed, stats['issues'], str(root / 'project_audit_report.txt'))
    # تصدير مخطط العلاقات
    if args.export_graph:
        export_graph(edges, str(root / 'dependency_graph'))
    console.print("[bold green]✅ تم تدقيق وتنظيم المشروع بنجاح! راجع التقرير: project_audit_report.txt[/bold green]")

if __name__ == '__main__':
    main()
