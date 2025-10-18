import time
import logging

class RecoveryManager:
    fallback_count = 0
    last_trigger_time = None

    @staticmethod
    def log_event(message):
        logging.basicConfig(filename="recovery.log", level=logging.INFO, format="%(asctime)s %(message)s")
        logging.info(f"[Recovery] {message}")
        RecoveryManager.last_trigger_time = time.time()

    @staticmethod
    def cooldown_ready(seconds=5):
        if RecoveryManager.last_trigger_time is None:
            return True
        return (time.time() - RecoveryManager.last_trigger_time) >= seconds

    @staticmethod
    def trigger_fallback(reason):
        RecoveryManager.fallback_count += 1
        RecoveryManager.log_event(f"Fallback triggered: {reason}")