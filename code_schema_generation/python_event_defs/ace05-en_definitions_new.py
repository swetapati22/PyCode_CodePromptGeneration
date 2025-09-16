from dataclasses import dataclass
from typing import List, Optional
from utils_typing import Entity, Event, Relation, dataclass


@dataclass
class MovementEvent:
    pass

@dataclass
class TransactionEvent:
    pass

@dataclass
class LifeEvent:
    pass

@dataclass
class PersonnelEvent:
    pass

@dataclass
class ConflictEvent:
    pass

@dataclass
class ContactEvent:
    pass

@dataclass
class JusticeEvent:
    pass

@dataclass
class BusinessEvent:
    pass

@dataclass
class Attack(ConflictEvent):
    def __init__(self, mention: Optional[str] = None, instrument: Optional[List] = None, target: Optional[List] = None, victim: Optional[List] = None, place: Optional[List] = None, agent: Optional[List] = None, attacker: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.instrument = instrument if instrument is not None else []
        self.target = target if target is not None else []
        self.victim = victim if victim is not None else []
        self.place = place if place is not None else []
        self.agent = agent if agent is not None else []
        self.attacker = attacker if attacker is not None else []
    def __repr__(self):
        return f"Attack(mention='{self.mention}', instrument={self.instrument}, target={self.target}, victim={self.victim}, place={self.place}, agent={self.agent}, attacker={self.attacker})"

@dataclass
class Meet(ContactEvent):
    def __init__(self, mention: Optional[str] = None, place: Optional[List] = None, entity: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.entity = entity if entity is not None else []
    def __repr__(self):
        return f"Meet(mention='{self.mention}', place={self.place}, entity={self.entity})"

@dataclass
class Transport(MovementEvent):
    def __init__(self, mention: Optional[str] = None, origin: Optional[List] = None, victim: Optional[List] = None, vehicle: Optional[List] = None, place: Optional[List] = None, agent: Optional[List] = None, destination: Optional[List] = None, artifact: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.origin = origin if origin is not None else []
        self.victim = victim if victim is not None else []
        self.vehicle = vehicle if vehicle is not None else []
        self.place = place if place is not None else []
        self.agent = agent if agent is not None else []
        self.destination = destination if destination is not None else []
        self.artifact = artifact if artifact is not None else []
    def __repr__(self):
        return f"Transport(mention='{self.mention}', origin={self.origin}, victim={self.victim}, vehicle={self.vehicle}, place={self.place}, agent={self.agent}, destination={self.destination}, artifact={self.artifact})"

@dataclass
class Demonstrate(ConflictEvent):
    def __init__(self, mention: Optional[str] = None, place: Optional[List] = None, entity: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.entity = entity if entity is not None else []
    def __repr__(self):
        return f"Demonstrate(mention='{self.mention}', place={self.place}, entity={self.entity})"

@dataclass
class Die(LifeEvent):
    def __init__(self, mention: Optional[str] = None, person: Optional[List] = None, instrument: Optional[List] = None, victim: Optional[List] = None, place: Optional[List] = None, agent: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.person = person if person is not None else []
        self.instrument = instrument if instrument is not None else []
        self.victim = victim if victim is not None else []
        self.place = place if place is not None else []
        self.agent = agent if agent is not None else []
    def __repr__(self):
        return f"Die(mention='{self.mention}', person={self.person}, instrument={self.instrument}, victim={self.victim}, place={self.place}, agent={self.agent})"

@dataclass
class Injure(LifeEvent):
    def __init__(self, mention: Optional[str] = None, instrument: Optional[List] = None, victim: Optional[List] = None, place: Optional[List] = None, agent: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.instrument = instrument if instrument is not None else []
        self.victim = victim if victim is not None else []
        self.place = place if place is not None else []
        self.agent = agent if agent is not None else []
    def __repr__(self):
        return f"Injure(mention='{self.mention}', instrument={self.instrument}, victim={self.victim}, place={self.place}, agent={self.agent})"

@dataclass
class EndPosition(PersonnelEvent):
    def __init__(self, mention: Optional[str] = None, place: Optional[List] = None, person: Optional[List] = None, entity: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.person = person if person is not None else []
        self.entity = entity if entity is not None else []
    def __repr__(self):
        return f"EndPosition(mention='{self.mention}', place={self.place}, person={self.person}, entity={self.entity})"

@dataclass
class StartPosition(PersonnelEvent):
    def __init__(self, mention: Optional[str] = None, place: Optional[List] = None, person: Optional[List] = None, entity: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.person = person if person is not None else []
        self.entity = entity if entity is not None else []
    def __repr__(self):
        return f"StartPosition(mention='{self.mention}', place={self.place}, person={self.person}, entity={self.entity})"

@dataclass
class StartOrg(BusinessEvent):
    def __init__(self, mention: Optional[str] = None, org: Optional[List] = None, agent: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.org = org if org is not None else []
        self.agent = agent if agent is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"StartOrg(mention='{self.mention}', org={self.org}, agent={self.agent}, place={self.place})"

@dataclass
class Elect(PersonnelEvent):
    def __init__(self, mention: Optional[str] = None, place: Optional[List] = None, person: Optional[List] = None, entity: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.person = person if person is not None else []
        self.entity = entity if entity is not None else []
    def __repr__(self):
        return f"Elect(mention='{self.mention}', place={self.place}, person={self.person}, entity={self.entity})"

@dataclass
class TransferMoney(TransactionEvent):
    def __init__(self, mention: Optional[str] = None, beneficiary: Optional[List] = None, giver: Optional[List] = None, recipient: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.giver = giver if giver is not None else []
        self.recipient = recipient if recipient is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"TransferMoney(mention='{self.mention}', beneficiary={self.beneficiary}, giver={self.giver}, recipient={self.recipient}, place={self.place})"

@dataclass
class Convict(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, defendant: Optional[List] = None, adjudicator: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.defendant = defendant if defendant is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"Convict(mention='{self.mention}', defendant={self.defendant}, adjudicator={self.adjudicator}, place={self.place})"

@dataclass
class Appeal(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, adjudicator: Optional[List] = None, plaintiff: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.plaintiff = plaintiff if plaintiff is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"Appeal(mention='{self.mention}', adjudicator={self.adjudicator}, plaintiff={self.plaintiff}, place={self.place})"

@dataclass
class TrialHearing(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, prosecutor: Optional[List] = None, defendant: Optional[List] = None, adjudicator: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.prosecutor = prosecutor if prosecutor is not None else []
        self.defendant = defendant if defendant is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"TrialHearing(mention='{self.mention}', prosecutor={self.prosecutor}, defendant={self.defendant}, adjudicator={self.adjudicator}, place={self.place})"

@dataclass
class Sentence(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, defendant: Optional[List] = None, adjudicator: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.defendant = defendant if defendant is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"Sentence(mention='{self.mention}', defendant={self.defendant}, adjudicator={self.adjudicator}, place={self.place})"

@dataclass
class PhoneWrite(ContactEvent):
    def __init__(self, mention: Optional[str] = None, place: Optional[List] = None, entity: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.entity = entity if entity is not None else []
    def __repr__(self):
        return f"PhoneWrite(mention='{self.mention}', place={self.place}, entity={self.entity})"

@dataclass
class ArrestJail(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, agent: Optional[List] = None, person: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.person = person if person is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"ArrestJail(mention='{self.mention}', agent={self.agent}, person={self.person}, place={self.place})"

@dataclass
class Acquit(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, defendant: Optional[List] = None, adjudicator: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.defendant = defendant if defendant is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
    def __repr__(self):
        return f"Acquit(mention='{self.mention}', defendant={self.defendant}, adjudicator={self.adjudicator})"

@dataclass
class ChargeIndict(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, prosecutor: Optional[List] = None, defendant: Optional[List] = None, adjudicator: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.prosecutor = prosecutor if prosecutor is not None else []
        self.defendant = defendant if defendant is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"ChargeIndict(mention='{self.mention}', prosecutor={self.prosecutor}, defendant={self.defendant}, adjudicator={self.adjudicator}, place={self.place})"

@dataclass
class Nominate(PersonnelEvent):
    def __init__(self, mention: Optional[str] = None, agent: Optional[List] = None, person: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.person = person if person is not None else []
    def __repr__(self):
        return f"Nominate(mention='{self.mention}', agent={self.agent}, person={self.person})"

@dataclass
class Fine(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, place: Optional[List] = None, adjudicator: Optional[List] = None, entity: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.entity = entity if entity is not None else []
    def __repr__(self):
        return f"Fine(mention='{self.mention}', place={self.place}, adjudicator={self.adjudicator}, entity={self.entity})"

@dataclass
class DeclareBankruptcy(BusinessEvent):
    def __init__(self, mention: Optional[str] = None, org: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.org = org if org is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"DeclareBankruptcy(mention='{self.mention}', org={self.org}, place={self.place})"

@dataclass
class TransferOwnership(TransactionEvent):
    def __init__(self, mention: Optional[str] = None, beneficiary: Optional[List] = None, buyer: Optional[List] = None, place: Optional[List] = None, seller: Optional[List] = None, artifact: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.buyer = buyer if buyer is not None else []
        self.place = place if place is not None else []
        self.seller = seller if seller is not None else []
        self.artifact = artifact if artifact is not None else []
    def __repr__(self):
        return f"TransferOwnership(mention='{self.mention}', beneficiary={self.beneficiary}, buyer={self.buyer}, place={self.place}, seller={self.seller}, artifact={self.artifact})"

@dataclass
class EndOrg(BusinessEvent):
    def __init__(self, mention: Optional[str] = None, org: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.org = org if org is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"EndOrg(mention='{self.mention}', org={self.org}, place={self.place})"

@dataclass
class Execute(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, agent: Optional[List] = None, person: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.agent = agent if agent is not None else []
        self.person = person if person is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"Execute(mention='{self.mention}', agent={self.agent}, person={self.person}, place={self.place})"

@dataclass
class ReleaseParole(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, place: Optional[List] = None, person: Optional[List] = None, entity: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.person = person if person is not None else []
        self.entity = entity if entity is not None else []
    def __repr__(self):
        return f"ReleaseParole(mention='{self.mention}', place={self.place}, person={self.person}, entity={self.entity})"

@dataclass
class MergeOrg(BusinessEvent):
    def __init__(self, mention: Optional[str] = None, org: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.org = org if org is not None else []
    def __repr__(self):
        return f"MergeOrg(mention='{self.mention}', org={self.org})"

@dataclass
class Marry(LifeEvent):
    def __init__(self, mention: Optional[str] = None, person: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.person = person if person is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"Marry(mention='{self.mention}', person={self.person}, place={self.place})"

@dataclass
class Divorce(LifeEvent):
    def __init__(self, mention: Optional[str] = None, person: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.person = person if person is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"Divorce(mention='{self.mention}', person={self.person}, place={self.place})"

@dataclass
class Sue(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, plaintiff: Optional[List] = None, defendant: Optional[List] = None, adjudicator: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.plaintiff = plaintiff if plaintiff is not None else []
        self.defendant = defendant if defendant is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"Sue(mention='{self.mention}', plaintiff={self.plaintiff}, defendant={self.defendant}, adjudicator={self.adjudicator}, place={self.place})"

@dataclass
class Pardon(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, defendant: Optional[List] = None, adjudicator: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.defendant = defendant if defendant is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"Pardon(mention='{self.mention}', defendant={self.defendant}, adjudicator={self.adjudicator}, place={self.place})"

@dataclass
class BeBorn(LifeEvent):
    def __init__(self, mention: Optional[str] = None, person: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.person = person if person is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"BeBorn(mention='{self.mention}', person={self.person}, place={self.place})"

@dataclass
class Extradite(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, person: Optional[List] = None, origin: Optional[List] = None, agent: Optional[List] = None, destination: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.person = person if person is not None else []
        self.origin = origin if origin is not None else []
        self.agent = agent if agent is not None else []
        self.destination = destination if destination is not None else []
    def __repr__(self):
        return f"Extradite(mention='{self.mention}', person={self.person}, origin={self.origin}, agent={self.agent}, destination={self.destination})"

