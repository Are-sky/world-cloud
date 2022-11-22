class MyResult:
    code = str;
    message = str;
    def __init__(self,code=None,message=None):
        self.code = code;
        self.message = message;

    def OK(self,message):
        self.message = message;
        self.code = "1";
        return self;

    def ERROR(self,message):
        self.message = message;
        self.code = "0";
        return self;

    def __str__(self) -> str:
        return "code: " + self.code + " message " + self.message
