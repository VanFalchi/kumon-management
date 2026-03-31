from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.jobs.jobs_cobrancas import gerar_cobranças_mensais
from app.jobs.jobs_boletos import emitir_boletos_digitais, verificar_inadimplencia

scheduler = BackgroundScheduler()

def iniciar_scheduler():
    scheduler.add_job(
        gerar_cobranças_mensais,
        CronTrigger(day=1, hour=6, minute=0),
        id="gerar_cobranças_mensais",
        replace_existing=True,
        misfire_grace_time=3600,
        coalesce=True
    )

    scheduler.add_job(
        emitir_boletos_digitais,
        CronTrigger(hour=8, minute=0),
        id="emitir_boletos_digitais",
        replace_existing=True,
        misfire_grace_time=3600,
        coalesce=True
    )

    scheduler.add_job(
        verificar_inadimplencia,
        CronTrigger(hour=9, minute=0),
        id="verificar_inadimplencia",
        replace_existing=True,
        misfire_grace_time=3600,
        coalesce=True
    )

    scheduler.start()
    print("Scheduler iniciado")

def parar_scheduler():
    scheduler.shutdown()
    print("Scheduler parado")