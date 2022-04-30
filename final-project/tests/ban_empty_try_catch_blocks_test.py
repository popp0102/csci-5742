def handled_exception():
    try:
        print("doing something useful, until...")
        raise Exception("Something happened!")
    except:
        print("but I'm handling it")

def unhandled_exception():
    try:
        print("doing something useful, until...")
        raise Exception("Something happened!")
    except NameError:
        # this comment doesn't bypass the check, this is still considered bad
        pass
    except Exception:
        pass
    except:
        pass

unhandled_exception()

