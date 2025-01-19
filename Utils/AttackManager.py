from typing import Callable
from ATTACKS.Attacks.AdminSectionAccess import AdminSectionAccess
from ATTACKS.Attacks.ExposeScoreBoard import ExposeScoreBoard
from ATTACKS.Attacks.ForgedFeedback import ForgedFeedback
from ATTACKS.Attacks.RetrieveOrders import RetrieveOrders

class Attack:
    def __init__(self, name: str, attack_type: str, run_function: Callable):
        self.name = name
        self.attack_type = attack_type
        self.run_function = run_function

class AttackManager:
    def __init__(self):
        self._attacks = {}

        # Ajoutez les attaques ici
        self._attacks["Admin Section Access"] = Attack(
            "Admin Section Access", "CONTROL_BROKEN", self._run_admin_section_access
        )
        self._attacks["Expose Score Board"] = Attack(
            "Expose Score Board", "DATA_EXPOSURE", self._run_expose_score_board
        )
        self._attacks["Forged Feedback"] = Attack(
            "Forged Feedback", "DATA_EXPOSURE", self._run_forged_feedback
        )
        self._attacks["Retrieve Orders"] = Attack(
            "Retrieve Orders", "CONTROL_BROKEN", self._run_retrieve_orders
        )

    def get_attacks(self):
        return self._attacks

    # Méthodes pour exécuter les attaques
    def _run_admin_section_access(self, url: str, callback: Callable = None):
        attack = AdminSectionAccess(url)
        if callback:
            callback(f"Running Admin Section Access on {url}")
        attack.run_exploit()
        if callback:
            callback("Admin Section Access completed")

    def _run_expose_score_board(self, url: str, callback: Callable = None):
        attack = ExposeScoreBoard(url)
        if callback:
            callback(f"Running Expose Score Board on {url}")
        attack.run_exploit()
        if callback:
            callback("Expose Score Board completed")

    def _run_forged_feedback(self, url: str, callback: Callable = None):
        attack = ForgedFeedback(url)
        if callback:
            callback(f"Running Forged Feedback on {url}")
        attack.run_exploit()
        if callback:
            callback("Forged Feedback completed")

    def _run_retrieve_orders(self, url: str, callback: Callable = None):
        attack = RetrieveOrders(url)
        if callback:
            callback(f"Running Retrieve Orders on {url}")
        attack.run_exploit()
        if callback:
            callback("Retrieve Orders completed")
