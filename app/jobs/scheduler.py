from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.jobs.jobs_cobrancas import gerar_cobranças_mensais

scheduler = BackgroundScheduler()

def iniciar_scheduler():
    scheduler.add_job(
        gerar_cobranças_mensais,
        CronTrigger(day=1, hour=6, minute=0),
        id="gerar_cobranças_mensais",
        replace_existing=True
    )
    scheduler.start()
    print("Scheduler iniciado")

def parar_scheduler():
    scheduler.shutdown()
    print("Scheduler parado")