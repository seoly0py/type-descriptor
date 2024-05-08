class TypeDiscriptor:

    def __init__(self, value) -> None:

        type_of_value = type(value)
        self.nullable = False
        self.rule = None
        self.origin = value

        if type_of_value in [int, float]:
            self.type = 'number'
        elif type_of_value == str:
            self.type = 'string'
        elif type_of_value == bool:
            self.type = 'boolean'
        elif type_of_value == dict:
            self.type = 'object'
            self.object_type = {}
            obj: dict = value
            for k, v in obj.items():
                self.object_type.update({ k: TypeDiscriptor(v) })
        elif type_of_value == list:
            self.type = 'array'
            arr: list = value
            is_united_type = True
            prev_type = 'null'
            for item in arr:
                if prev_type == 'null':
                    prev_type = TypeDiscriptor(item)
                else:
                    is_united_type = is_united_type and TypeDiscriptor(item) == prev_type
            if is_united_type:
                self.element_type = prev_type
            else:
                self.element_type = 'unkown'
        else:
            if type_of_value == type(None):
                self.type = 'null'
            else:
                pass

    def __eq__(self, value: 'TypeDiscriptor') -> bool:

        if type(value) != TypeDiscriptor:
            return False

        if self.type == 'rule':
            return self.rule(value.origin)
        elif value.type =='rule':
            return value.rule(self.origin)
        
        if self.type == 'null' and value.nullable == True or value.type == 'null' and self.nullable == True:
            return True

        if self.type in ['number', 'string', 'boolean', 'unkown']:
            if self.nullable == True or value.nullable == True:
                return True
            return self.type == value.type
        elif self.type == 'array' and value.type == 'array':
            if self.element_type == 'null' or value.element_type == 'null':
                return True
            return self.element_type == value.element_type
        elif self.type == 'object' and value.type == 'object':
            self_type_keys = set(self.object_type.keys())
            target_type_keys = set(value.object_type.keys())

            if self_type_keys != target_type_keys:
                return False

            result = True
            for k, v in self.object_type.items():
                result = result and (v == value.object_type.get(k))
            return result
        else:
            return False
    
    @staticmethod
    def Any():
        descriptor = TypeDiscriptor(None)
        descriptor.type = 'null'
        return descriptor

    @staticmethod
    def Object(objectType):
        descriptor = TypeDiscriptor(None)
        descriptor.type = 'object'
        descriptor.object_type = objectType
        return descriptor
    
    @staticmethod
    def Array(elementType):
        descriptor = TypeDiscriptor(None)
        descriptor.type = 'array'
        descriptor.element_type = elementType
        return descriptor
    
    @staticmethod
    def String(nullable=False):
        descriptor = TypeDiscriptor(None)
        descriptor.nullable = nullable
        descriptor.type = 'string'
        return descriptor
    
    @staticmethod
    def Number(nullable=False):
        descriptor = TypeDiscriptor(None)
        descriptor.nullable = nullable
        descriptor.type = 'number'
        return descriptor
    
    @staticmethod
    def Boolean(nullable=False):
        descriptor = TypeDiscriptor(None)
        descriptor.nullable = nullable
        descriptor.type = 'boolean'
        return descriptor
    
    @staticmethod
    def Rule(rule):
        descriptor = TypeDiscriptor(None)
        descriptor.type = 'rule'
        descriptor.rule = rule
        return descriptor