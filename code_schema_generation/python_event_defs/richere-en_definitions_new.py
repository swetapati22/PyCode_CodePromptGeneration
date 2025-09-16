from dataclasses import dataclass
from typing import List, Optional
from utils_typing import Entity, Event, Relation, dataclass


@dataclass
class JusticeEvent:
    pass

@dataclass
class ManufactureEvent:
    pass

@dataclass
class PersonnelEvent:
    pass

@dataclass
class BusinessEvent:
    pass

@dataclass
class ContactEvent:
    pass

@dataclass
class MovementEvent:
    pass

@dataclass
class ConflictEvent:
    pass

@dataclass
class LifeEvent:
    pass

@dataclass
class TransactionEvent:
    pass

@dataclass
class Nominate(PersonnelEvent):
    def __init__(self, mention: Optional[str] = None, place: Optional[List] = None, person: Optional[List] = None, agent: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.person = person if person is not None else []
        self.agent = agent if agent is not None else []
    def __repr__(self):
        return f"Nominate(mention='{self.mention}', place={self.place}, person={self.person}, agent={self.agent})"

@dataclass
class Meet(ContactEvent):
    def __init__(self, mention: Optional[str] = None, entity: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.entity = entity if entity is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"Meet(mention='{self.mention}', entity={self.entity}, place={self.place})"

@dataclass
class Marry(LifeEvent):
    def __init__(self, mention: Optional[str] = None, place: Optional[List] = None, person: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.person = person if person is not None else []
    def __repr__(self):
        return f"Marry(mention='{self.mention}', place={self.place}, person={self.person})"

@dataclass
class Divorce(LifeEvent):
    def __init__(self, mention: Optional[str] = None, place: Optional[List] = None, person: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.person = person if person is not None else []
    def __repr__(self):
        return f"Divorce(mention='{self.mention}', place={self.place}, person={self.person})"

@dataclass
class Elect(PersonnelEvent):
    def __init__(self, mention: Optional[str] = None, place: Optional[List] = None, person: Optional[List] = None, agent: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.person = person if person is not None else []
        self.agent = agent if agent is not None else []
    def __repr__(self):
        return f"Elect(mention='{self.mention}', place={self.place}, person={self.person}, agent={self.agent})"

@dataclass
class Correspondence(ContactEvent):
    def __init__(self, mention: Optional[str] = None, entity: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.entity = entity if entity is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"Correspondence(mention='{self.mention}', entity={self.entity}, place={self.place})"

@dataclass
class TrialHearing(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, adjudicator: Optional[List] = None, prosecutor: Optional[List] = None, defendant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.prosecutor = prosecutor if prosecutor is not None else []
        self.defendant = defendant if defendant is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"TrialHearing(mention='{self.mention}', adjudicator={self.adjudicator}, prosecutor={self.prosecutor}, defendant={self.defendant}, place={self.place})"

@dataclass
class EndPosition(PersonnelEvent):
    def __init__(self, mention: Optional[str] = None, entity: Optional[List] = None, place: Optional[List] = None, person: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.entity = entity if entity is not None else []
        self.place = place if place is not None else []
        self.person = person if person is not None else []
    def __repr__(self):
        return f"EndPosition(mention='{self.mention}', entity={self.entity}, place={self.place}, person={self.person})"

@dataclass
class Die(LifeEvent):
    def __init__(self, mention: Optional[str] = None, place: Optional[List] = None, instrument: Optional[List] = None, victim: Optional[List] = None, agent: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.instrument = instrument if instrument is not None else []
        self.victim = victim if victim is not None else []
        self.agent = agent if agent is not None else []
    def __repr__(self):
        return f"Die(mention='{self.mention}', place={self.place}, instrument={self.instrument}, victim={self.victim}, agent={self.agent})"

@dataclass
class Attack(ConflictEvent):
    def __init__(self, mention: Optional[str] = None, target: Optional[List] = None, attacker: Optional[List] = None, instrument: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.target = target if target is not None else []
        self.attacker = attacker if attacker is not None else []
        self.instrument = instrument if instrument is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"Attack(mention='{self.mention}', target={self.target}, attacker={self.attacker}, instrument={self.instrument}, place={self.place})"

@dataclass
class Injure(LifeEvent):
    def __init__(self, mention: Optional[str] = None, place: Optional[List] = None, instrument: Optional[List] = None, victim: Optional[List] = None, agent: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.instrument = instrument if instrument is not None else []
        self.victim = victim if victim is not None else []
        self.agent = agent if agent is not None else []
    def __repr__(self):
        return f"Injure(mention='{self.mention}', place={self.place}, instrument={self.instrument}, victim={self.victim}, agent={self.agent})"

@dataclass
class ChargeIndict(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, adjudicator: Optional[List] = None, prosecutor: Optional[List] = None, defendant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.prosecutor = prosecutor if prosecutor is not None else []
        self.defendant = defendant if defendant is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"ChargeIndict(mention='{self.mention}', adjudicator={self.adjudicator}, prosecutor={self.prosecutor}, defendant={self.defendant}, place={self.place})"

@dataclass
class Acquit(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, adjudicator: Optional[List] = None, place: Optional[List] = None, defendant: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.place = place if place is not None else []
        self.defendant = defendant if defendant is not None else []
    def __repr__(self):
        return f"Acquit(mention='{self.mention}', adjudicator={self.adjudicator}, place={self.place}, defendant={self.defendant})"

@dataclass
class ArrestJail(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, place: Optional[List] = None, person: Optional[List] = None, agent: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.person = person if person is not None else []
        self.agent = agent if agent is not None else []
    def __repr__(self):
        return f"ArrestJail(mention='{self.mention}', place={self.place}, person={self.person}, agent={self.agent})"

@dataclass
class ReleaseParole(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, place: Optional[List] = None, person: Optional[List] = None, agent: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.person = person if person is not None else []
        self.agent = agent if agent is not None else []
    def __repr__(self):
        return f"ReleaseParole(mention='{self.mention}', place={self.place}, person={self.person}, agent={self.agent})"

@dataclass
class Convict(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, adjudicator: Optional[List] = None, place: Optional[List] = None, defendant: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.place = place if place is not None else []
        self.defendant = defendant if defendant is not None else []
    def __repr__(self):
        return f"Convict(mention='{self.mention}', adjudicator={self.adjudicator}, place={self.place}, defendant={self.defendant})"

@dataclass
class TransportPerson(MovementEvent):
    def __init__(self, mention: Optional[str] = None, origin: Optional[List] = None, destination: Optional[List] = None, instrument: Optional[List] = None, person: Optional[List] = None, agent: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.origin = origin if origin is not None else []
        self.destination = destination if destination is not None else []
        self.instrument = instrument if instrument is not None else []
        self.person = person if person is not None else []
        self.agent = agent if agent is not None else []
    def __repr__(self):
        return f"TransportPerson(mention='{self.mention}', origin={self.origin}, destination={self.destination}, instrument={self.instrument}, person={self.person}, agent={self.agent})"

@dataclass
class TransferMoney(TransactionEvent):
    def __init__(self, mention: Optional[str] = None, giver: Optional[List] = None, recipient: Optional[List] = None, beneficiary: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.giver = giver if giver is not None else []
        self.recipient = recipient if recipient is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"TransferMoney(mention='{self.mention}', giver={self.giver}, recipient={self.recipient}, beneficiary={self.beneficiary}, place={self.place})"

@dataclass
class Contact(ContactEvent):
    def __init__(self, mention: Optional[str] = None, entity: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.entity = entity if entity is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"Contact(mention='{self.mention}', entity={self.entity}, place={self.place})"

@dataclass
class EndOrg(BusinessEvent):
    def __init__(self, mention: Optional[str] = None, org: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.org = org if org is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"EndOrg(mention='{self.mention}', org={self.org}, place={self.place})"

@dataclass
class Sentence(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, adjudicator: Optional[List] = None, place: Optional[List] = None, defendant: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.place = place if place is not None else []
        self.defendant = defendant if defendant is not None else []
    def __repr__(self):
        return f"Sentence(mention='{self.mention}', adjudicator={self.adjudicator}, place={self.place}, defendant={self.defendant})"

@dataclass
class Appeal(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, adjudicator: Optional[List] = None, prosecutor: Optional[List] = None, defendant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.prosecutor = prosecutor if prosecutor is not None else []
        self.defendant = defendant if defendant is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"Appeal(mention='{self.mention}', adjudicator={self.adjudicator}, prosecutor={self.prosecutor}, defendant={self.defendant}, place={self.place})"

@dataclass
class Broadcast(ContactEvent):
    def __init__(self, mention: Optional[str] = None, entity: Optional[List] = None, place: Optional[List] = None, audience: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.entity = entity if entity is not None else []
        self.place = place if place is not None else []
        self.audience = audience if audience is not None else []
    def __repr__(self):
        return f"Broadcast(mention='{self.mention}', entity={self.entity}, place={self.place}, audience={self.audience})"

@dataclass
class TransferOwnership(TransactionEvent):
    def __init__(self, mention: Optional[str] = None, giver: Optional[List] = None, thing: Optional[List] = None, recipient: Optional[List] = None, beneficiary: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.giver = giver if giver is not None else []
        self.thing = thing if thing is not None else []
        self.recipient = recipient if recipient is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"TransferOwnership(mention='{self.mention}', giver={self.giver}, thing={self.thing}, recipient={self.recipient}, beneficiary={self.beneficiary}, place={self.place})"

@dataclass
class BeBorn(LifeEvent):
    def __init__(self, mention: Optional[str] = None, place: Optional[List] = None, person: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.person = person if person is not None else []
    def __repr__(self):
        return f"BeBorn(mention='{self.mention}', place={self.place}, person={self.person})"

@dataclass
class TransportArtifact(MovementEvent):
    def __init__(self, mention: Optional[str] = None, origin: Optional[List] = None, artifact: Optional[List] = None, destination: Optional[List] = None, agent: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.origin = origin if origin is not None else []
        self.artifact = artifact if artifact is not None else []
        self.destination = destination if destination is not None else []
        self.agent = agent if agent is not None else []
    def __repr__(self):
        return f"TransportArtifact(mention='{self.mention}', origin={self.origin}, artifact={self.artifact}, destination={self.destination}, agent={self.agent})"

@dataclass
class StartOrg(BusinessEvent):
    def __init__(self, mention: Optional[str] = None, org: Optional[List] = None, place: Optional[List] = None, agent: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.org = org if org is not None else []
        self.place = place if place is not None else []
        self.agent = agent if agent is not None else []
    def __repr__(self):
        return f"StartOrg(mention='{self.mention}', org={self.org}, place={self.place}, agent={self.agent})"

@dataclass
class DeclareBankruptcy(BusinessEvent):
    def __init__(self, mention: Optional[str] = None, org: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.org = org if org is not None else []
    def __repr__(self):
        return f"DeclareBankruptcy(mention='{self.mention}', org={self.org})"

@dataclass
class Artifact(ManufactureEvent):
    def __init__(self, mention: Optional[str] = None, place: Optional[List] = None, artifact: Optional[List] = None, agent: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.artifact = artifact if artifact is not None else []
        self.agent = agent if agent is not None else []
    def __repr__(self):
        return f"Artifact(mention='{self.mention}', place={self.place}, artifact={self.artifact}, agent={self.agent})"

@dataclass
class StartPosition(PersonnelEvent):
    def __init__(self, mention: Optional[str] = None, entity: Optional[List] = None, place: Optional[List] = None, person: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.entity = entity if entity is not None else []
        self.place = place if place is not None else []
        self.person = person if person is not None else []
    def __repr__(self):
        return f"StartPosition(mention='{self.mention}', entity={self.entity}, place={self.place}, person={self.person})"

@dataclass
class MergeOrg(BusinessEvent):
    def __init__(self, mention: Optional[str] = None, org: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.org = org if org is not None else []
    def __repr__(self):
        return f"MergeOrg(mention='{self.mention}', org={self.org})"

@dataclass
class Transaction(TransactionEvent):
    def __init__(self, mention: Optional[str] = None, giver: Optional[List] = None, recipient: Optional[List] = None, beneficiary: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.giver = giver if giver is not None else []
        self.recipient = recipient if recipient is not None else []
        self.beneficiary = beneficiary if beneficiary is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"Transaction(mention='{self.mention}', giver={self.giver}, recipient={self.recipient}, beneficiary={self.beneficiary}, place={self.place})"

@dataclass
class Sue(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, adjudicator: Optional[List] = None, plaintiff: Optional[List] = None, defendant: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.plaintiff = plaintiff if plaintiff is not None else []
        self.defendant = defendant if defendant is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"Sue(mention='{self.mention}', adjudicator={self.adjudicator}, plaintiff={self.plaintiff}, defendant={self.defendant}, place={self.place})"

@dataclass
class Extradite(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, origin: Optional[List] = None, destination: Optional[List] = None, person: Optional[List] = None, agent: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.origin = origin if origin is not None else []
        self.destination = destination if destination is not None else []
        self.person = person if person is not None else []
        self.agent = agent if agent is not None else []
    def __repr__(self):
        return f"Extradite(mention='{self.mention}', origin={self.origin}, destination={self.destination}, person={self.person}, agent={self.agent})"

@dataclass
class Fine(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, adjudicator: Optional[List] = None, entity: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.entity = entity if entity is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"Fine(mention='{self.mention}', adjudicator={self.adjudicator}, entity={self.entity}, place={self.place})"

@dataclass
class Demonstrate(ConflictEvent):
    def __init__(self, mention: Optional[str] = None, entity: Optional[List] = None, place: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.entity = entity if entity is not None else []
        self.place = place if place is not None else []
    def __repr__(self):
        return f"Demonstrate(mention='{self.mention}', entity={self.entity}, place={self.place})"

@dataclass
class Pardon(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, adjudicator: Optional[List] = None, place: Optional[List] = None, defendant: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.adjudicator = adjudicator if adjudicator is not None else []
        self.place = place if place is not None else []
        self.defendant = defendant if defendant is not None else []
    def __repr__(self):
        return f"Pardon(mention='{self.mention}', adjudicator={self.adjudicator}, place={self.place}, defendant={self.defendant})"

@dataclass
class Execute(JusticeEvent):
    def __init__(self, mention: Optional[str] = None, place: Optional[List] = None, person: Optional[List] = None, agent: Optional[List] = None):
        self.mention = mention if mention is not None else []
        self.place = place if place is not None else []
        self.person = person if person is not None else []
        self.agent = agent if agent is not None else []
    def __repr__(self):
        return f"Execute(mention='{self.mention}', place={self.place}, person={self.person}, agent={self.agent})"

