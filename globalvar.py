class GlobalVar:
    headers = None
def set_demo_value(value):
    GlobalVar.headers= value
def get_demo_value():
    return GlobalVar.headers