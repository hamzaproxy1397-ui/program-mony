# -*- coding: utf-8 -*-
"""
مدير المهام المجدولة للبرنامج المحاسبي
Scheduler Manager for Accounting Software
"""

import threading
import time
from datetime import datetime

class SchedulerManager:
    """مدير المهام المجدولة"""
    
    def __init__(self):
        self.running = False
        self.tasks = []
        self.thread = None
    
    def start(self):
        """بدء تشغيل المجدول"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()
            print("✅ تم بدء تشغيل مدير المهام المجدولة")
    
    def stop(self):
        """إيقاف المجدول"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        print("⏹️ تم إيقاف مدير المهام المجدولة")
    
    def add_task(self, task_func, interval=60):
        """إضافة مهمة جديدة"""
        self.tasks.append({
            'func': task_func,
            'interval': interval,
            'last_run': 0
        })
    
    def _run(self):
        """تشغيل المهام المجدولة"""
        while self.running:
            current_time = time.time()
            
            for task in self.tasks:
                if current_time - task['last_run'] >= task['interval']:
                    try:
                        task['func']()
                        task['last_run'] = current_time
                    except Exception as e:
                        print(f"خطأ في تنفيذ المهمة المجدولة: {e}")
            
            time.sleep(1)  # فحص كل ثانية
