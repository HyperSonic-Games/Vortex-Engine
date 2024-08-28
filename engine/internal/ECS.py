import uuid
from typing import Dict, Type

class Entity:
    """
    Represents a unique entity in the game.
    Each entity is identified by a unique UUID.
    """
    def __init__(self):
        self.Id = uuid.uuid4()  # Generate a unique identifier for the entity
        self.Components: Dict[Type['BaseComponent'], 'BaseComponent'] = {}  # Dictionary to store components by type

    def AddComponent(self, component: 'BaseComponent'):
        """
        Adds a component to the entity.
        :param component: An instance of a BaseComponent subclass.
        """
        componentType = type(component)
        self.Components[componentType] = component
        print(f"Added {componentType.__name__} to {self}")

    def RemoveComponent(self, componentType: Type['BaseComponent']):
        """
        Removes a component from the entity.
        :param componentType: The type of the component to remove.
        """
        if componentType in self.Components:
            del self.Components[componentType]
            print(f"Removed {componentType.__name__} from {self}")

    def GetComponent(self, componentType: Type['BaseComponent']) -> 'BaseComponent':
        """
        Retrieves a component from the entity.
        :param componentType: The type of the component to retrieve.
        :return: An instance of the component if it exists, else None.
        """
        return self.Components.get(componentType, None)

    def __repr__(self):
        return f"Entity({self.Id})"

class BaseComponent:
    """
    Base class for all components in the ECS.
    Components are plain data holders and do not have any behavior.
    """
    def __init__(self):
        self.Entity: Entity = None  # Reference to the entity that owns this component

    def __repr__(self):
        return f"{self.__class__.__name__}()"


# Position Component
class PositionComponent(BaseComponent):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.X = x
        self.Y = y

    def __repr__(self):
        return f"PositionComponent(X={self.X}, Y={self.Y})"

# Velocity Component
class VelocityComponent(BaseComponent):
    def __init__(self, vx: float, vy: float):
        super().__init__()
        self.Vx = vx
        self.Vy = vy

    def __repr__(self):
        return f"VelocityComponent(Vx={self.Vx}, Vy={self.Vy})"