class ParserFailed(Exception):
    """パースに失敗したエラー"""
    pass

class SystemWarn(Exception):
    """危険な入力が見つかった時"""
    pass

class MakerFailed(Exception):
    """Maker内の処理が失敗したときのエラー"""
    pass
