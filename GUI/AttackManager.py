# attack_manager.py
from dataclasses import dataclass
from typing import Callable, Dict, List
import logging

@dataclass
class Attack:
    name: str
    function: str  # Changé en str car c'est le nom de la fonction
    order: int
    description: str
    requires: List[str] = None
    button_style: str = 'default'
    button_row: int = 0
    button_column: int = 0
    status: str = 'pending'

class AttackManager:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
        self.logger = logging.getLogger(__name__)
        self.attacks: Dict[str, Attack] = {}
        self._register_default_attacks()

    def _register_default_attacks(self):
        self.register_attack(
            name="SPIDER",
            function="run_spider",
            order=1,
            description="Map application endpoints"
        )

        self.register_attack(
            name="JWT",
            function="run_jwt_attack",
            order=2,
            description="Forge admin JWT token",
            button_row=0,
            button_column=1
        )

        self.register_attack(
            name="SQL",
            function="run_sql_injection",
            order=3,
            description="Test SQL injection vulnerabilities",
            button_row=0,
            button_column=2
        )

        self.register_attack(
            name="CAPTCHA",
            function="run_captcha_bypass",
            order=4,
            description="Bypass CAPTCHA protection",
            button_row=1,
            button_column=0
        )

        self.register_attack(
            name="COUPON",
            function="run_coupon_exploit",
            order=5,
            description="Exploit coupon mechanism",
            button_row=1,
            button_column=1
        )

        self.register_attack(
            name="XXE",
            function="run_xxe_attack",
            order=6,
            description="Test XXE vulnerabilities",
            button_row=1,
            button_column=2
        )

        self.register_attack(
            name="XSS",
            function="run_xss_attacks",
            order=7,
            description="Test XSS vectors",
            button_row=2,
            button_column=0
        )

        self.register_attack(
            name="APIScrapper",
            function="run_spider",
            order=1,
            description="Map application endpoints"
        )

    def register_attack(self, name: str, function: str, order: int, description: str,
                       requires: List[str] = None, button_style: str = 'default',
                       button_row: int = 0, button_column: int = 0):
        self.attacks[name] = Attack(
            name=name,
            function=function,
            order=order,
            description=description,
            requires=requires or [],
            button_style=button_style,
            button_row=button_row,
            button_column=button_column
        )
        self.logger.debug(f"Registered attack: {name}")

    def update_attack_status(self, name: str, status: str):
        if name in self.attacks:
            self.attacks[name].status = status
            self.logger.info(f"Attack {name} status updated to {status}")
            return True
        self.logger.warning(f"Attempted to update status for unknown attack: {name}")
        return False

    def get_attack_sequence(self) -> List[Attack]:
        return sorted(self.attacks.values(), key=lambda x: x.order)

    def get_button_config(self) -> List[Dict]:
        return [
            {
                "name": attack.name,
                "row": attack.button_row,
                "column": attack.button_column,
                "style": attack.button_style,
                "description": attack.description
            }
            for attack in self.attacks.values()
        ]
        

    def can_run_attack(self, attack_name: str, completed_attacks: List[str]) -> bool:
        attack = self.attacks.get(attack_name)
        if not attack:
            self.logger.warning(f"Unknown attack: {attack_name}")
            return False

        dependencies_met = all(req in completed_attacks for req in (attack.requires or []))
        self.logger.debug(f"Checking attack: {attack_name}")
        self.logger.debug(f"Completed attacks: {completed_attacks}")
        self.logger.debug(f"Dependencies for {attack_name}: {attack.requires}")
        if not dependencies_met:
            self.logger.info(f"Missing dependencies for {attack_name}: {attack.requires}")
        return dependencies_met or not attack.requires
