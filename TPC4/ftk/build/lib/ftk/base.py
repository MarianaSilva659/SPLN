import re
from abc import abstractmethod, ABC
from typing import Iterable, Any

from collections import Counter
from enum import Enum

from probability import AbsoluteProbability


class TokenKind(Enum):
    WORD = 1
    STOP_WORD = 2
    PUNCTUATION = 3


class Token:
    def __init__(self, src: str, kind: TokenKind):
        self.src = src
        self.kind = kind

    def __repr__(self):
        return self.src


class AbstractLexer(ABC):
    @abstractmethod
    def lex(self, txt: str) -> Iterable[Token]:
        pass


class DefaultLexer(AbstractLexer):
    def lex(self, txt: str) -> Iterable[Token]:
        # FIXME patterns stopwords lems
        for it in re.finditer(r'(\w+(?:-\w+)*)|([^\w\s]+)', txt):
            if it[0] is not None:
                value = it[0]
                kind = TokenKind.WORD
            else:
                value = it[1]
                kind = TokenKind.PUNCTUATION
            yield Token(value, kind)


class AbstractStage(ABC):
    @abstractmethod
    def apply(self, item: Any) -> Any:
        pass


class AbstractReductionStage(ABC):
    @abstractmethod
    def apply(self, items: Iterable[Any]) -> Any:
        pass


class IdentityReductionStage(AbstractReductionStage):
    def apply(self, items: Iterable[Any]) -> Any:
        return items


class Pipeline:
    def __init__(self):
        self.lexer = DefaultLexer()
        self.stages = []
        self.reduction = IdentityReductionStage()

    def set_lexer(self, lexer: AbstractLexer):
        self.lexer = lexer

    def add_stage(self, stage: AbstractStage):
        self.stages.append(stage)

    def set_reduction(self, reduction: AbstractReductionStage):
        self.reduction = reduction

    def apply(self, txt: str) -> Any:
        tokens = self.lexer.lex(txt)

        for stage in self.stages:
            tokens = map(stage.apply, tokens)

        return self.reduction.apply(tokens)


class Convert2ProbabilityStage(AbstractReductionStage):
    def apply(self, items: Iterable[Any]) -> Any:
        c = Counter(map(lambda i: i.src, items))
        total = c.total()
        return {item: AbsoluteProbability(count, total) for item, count in c.items()}
