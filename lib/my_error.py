class ParserFailed(Exception):
    """パースに失敗したエラー"""
    pass

class WarnEmptyEQ(Exception):
    pass

class WarnEmptyVAR(Exception):
    pass

class SystemWarn(Exception):
    pass

class MakerFailed(Exception):
    """Maker内の処理が失敗したときのエラー"""
    pass
