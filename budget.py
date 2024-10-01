

from collections import namedtuple
import enum


payment = namedtuple('payment', ['people', 'amount'])


class P(enum.Enum):
    """
    Enum pro lidi
    """
    Milda : str = 'Milda'
    Anet : str = 'Anet'
    Kopy : str = 'Kopy'
    Misa : str = 'Misa'
    Leo : str = 'Leo'
    Honza : str = 'Honza'
    Toman : str = 'Toman'
    Kastan : str = 'Kastan'
    Baja : str = 'Baja'
    Panc : str = 'Panc'
    Nela : str = 'Nela'
    Soky : str = 'Soky'
    Ala : str = 'Ala'
    Adelka : str = 'Adelka'
    Barka : str = 'Barka'
    Fanda : str = 'Fanda'
    Tom : str = 'Tom'

# Jmeno, kolik dni
PEOPLE = {
    (P.Milda, 3),
    (P.Anet, 3),
    (P.Kopy, 6),
    (P.Misa, 6),
    (P.Leo, 6),
    (P.Honza, 6),
    (P.Toman, 5),
    (P.Kastan, 5),
    (P.Baja,  6),
    (P.Panc, 6),
    (P.Nela, 6),
    (P.Soky, 6),
    (P.Ala, 6),
    (P.Adelka, 6),
    (P.Barka, 3),
    (P.Fanda, 3),
    (P.Tom, 2),
}


class PersonInfo:
    """
    Info k jedne osobe, kdo kolik zaplatil a kolik ma zaplatit
    """
    paid: int = 0
    to_pay: int = 0

    def __str__(self) -> str:
        pad = "" if self.to_pay < 0 else " "
        pad2 = " " if self.to_pay < 0 else ""
        return f'paid: {self.paid}{" " * (7-len(str(int(self.paid))))} to_pay: {pad}{self.to_pay:.2f}{" " * (5-len(str(int(self.to_pay))))}    {pad2}days: {self.days}'

    def __init__(self, days: int) -> None:
        self.days = days


payments: list[tuple[tuple[str], int]] = [
    # Jidlo
    payment((P.Anet, P.Milda), 1650),
    payment((P.Kopy, P.Misa), 1600),
    payment((P.Honza,), 800), # segedin
    payment((P.Toman,), 1680),
    payment((P.Ala, P.Soky), 1400),
    payment((P.Baja,), 1200),
    payment((P.Honza,), 900), # Ada - burty na pivu, platil JJ
    payment((P.Panc, P.Nela), 1500),
    # Ostatni vydaje
    payment((P.Kastan,), 150),
    payment((P.Baja,), 1200),
    payment((P.Baja,), 300),
    payment((P.Toman,), 80),
    payment((P.Toman,), 250),
    payment((P.Toman,), 550),
    payment((P.Panc, P.Nela), 700),
    payment((P.Honza,), 2000),
]

max_days = 6
budget = sum([payment.amount for payment in payments])
total_days = sum([person[1] for person in PEOPLE])
# mapa jmena na person info
people_info: dict[str, PersonInfo] = {P(person[0].name): PersonInfo(person[1]) for person in PEOPLE}


def count() -> None:
    """
    Zpracuje vsechny platby a vypocita kolik kdo ma zaplatit
    """
    for payment in payments:
        _add_payment(payment)
    for person, info in people_info.items():
        info.to_pay = _budget_share(person) - info.paid

def _add_payment(payment: payment):
    """
    Zpracuje jednu platbu
    """
    payment_split = payment.amount // len(payment.people)
    for person in payment.people:
        people_info[person].paid += payment_split
    

def _budget_share(person: str) -> int:
    """
    Vrati fin. podil osoby na celkovem rozpoctu
    """
    info = people_info[person]
    budget_days_ratio = (info.days / total_days)
    share = budget * budget_days_ratio
    # print(f'{person.name} budget share: {g}, ratio: {budget_days_ratio}')
    return share


if __name__ == '__main__':
    count()
    for person, info in people_info.items():
        print(f'{person.name}:{" " * (10-len(person.name))}   {info}')
    print(f'Celkovy rozpocet: {budget}')
    # a = sorted(list(people_info.values()),key=lambda x: x.to_pay)
    
    # Sum of `to_pay` of all attendands must always be 0.0
    assert not (sum([info.to_pay for info in people_info.values()]))
