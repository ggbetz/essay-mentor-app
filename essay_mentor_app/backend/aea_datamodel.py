# argumentative essay analysis data model

from typing import List

import uuid
import dataclasses


@dataclasses.dataclass
class BaseContentItem:
    text: str
    uid: str = dataclasses.field(init=False)

    def __post_init__(self):
        self.uid = str(uuid.uuid4())


@dataclasses.dataclass
class EssayContentItem(BaseContentItem):
    name: str
    html: str
    heading_level: int = 0


@dataclasses.dataclass
class MainQuestion(BaseContentItem):
    claim_refs: List[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class MainClaim(BaseContentItem):
    question_refs: List[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Reason(BaseContentItem):
    parent_uid: str
    essay_text_refs: List[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class ArgumentativeEssayAnalysis:
    essaytext_md: str = ""
    essaytext_html: str = ""
    essay_content_items: List[EssayContentItem] = dataclasses.field(default_factory=list)
    main_questions: List[MainQuestion] = dataclasses.field(default_factory=list)
    main_claims: List[MainClaim] = dataclasses.field(default_factory=list)
    reasons: List[Reason] = dataclasses.field(default_factory=list)
    objections: List[Reason] = dataclasses.field(default_factory=list)
    rebuttals: List[Reason] = dataclasses.field(default_factory=list)