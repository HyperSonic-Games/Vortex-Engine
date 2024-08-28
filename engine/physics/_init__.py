"""
numba jit compiled physics engine with multithreading
"""

import numpy as np
from numba import njit, prange
from scipy.spatial.transform import Rotation as R
from ..internal.ECS import Entity, PositionComponent, VelocityComponent

# Constants
Gravity = 9.81
TimeStep = 0.01

@njit(parallel=True)
def UpdatePositions(entities, numEntities):
    """
    Update the positions and velocities of entities based on physics.
    
    :param entities: A 2D numpy array where each row contains position and velocity vectors.
    :param numEntities: Number of entities in the simulation.
    """
    for i in prange(numEntities):
        position = entities[i][0]
        velocity = entities[i][1]
        position[0] += velocity[0] * TimeStep
        position[1] += velocity[1] * TimeStep
        velocity[1] -= Gravity * TimeStep

@njit(parallel=True)
def ApplyCollisions(entities, numEntities, width, height):
    """
    Handle collisions with the boundaries of the simulation area.
    
    :param entities: A 2D numpy array where each row contains position and velocity vectors.
    :param numEntities: Number of entities in the simulation.
    :param width: Width of the simulation area.
    :param height: Height of the simulation area.
    """
    for i in prange(numEntities):
        position = entities[i][0]
        velocity = entities[i][1]
        if position[0] < 0 or position[0] > width:
            velocity[0] *= -1
        if position[1] < 0 or position[1] > height:
            velocity[1] *= -1

def RotateVelocity(velocity, angle):
    """
    Rotates the velocity vector by a given angle.
    
    :param velocity: A 2D numpy array representing the velocity vector.
    :param angle: Rotation angle in degrees.
    :return: The rotated velocity vector.
    """
    rotation = R.from_euler('z', angle, degrees=True)
    return rotation.apply(velocity)

def Simulate(entities, width, height):
    """
    Run the simulation by updating positions, applying collisions, and rotating velocities.
    
    :param entities: List of Entity objects.
    :param width: Width of the simulation area.
    :param height: Height of the simulation area.
    """
    numEntities = len(entities)
    
    # Convert entities to numpy arrays for Numba functions
    entityData = []
    for e in entities:
        posComp = e.GetComponent(PositionComponent)
        velComp = e.GetComponent(VelocityComponent)
        
        if posComp is None or velComp is None:
            print(f"Entity {e.Id} is missing components. Skipping.")
            continue
        
        entityData.append([np.array([posComp.X, posComp.Y]), np.array([velComp.Vx, velComp.Vy])])
    
    if not entityData:
        print("No valid entities to simulate.")
        return
    
    entityData = np.array(entityData)
    
    UpdatePositions(entityData, numEntities)
    ApplyCollisions(entityData, numEntities, width, height)
    
    # Example of rotating velocity of all entities
    for i in range(numEntities):
        velocity = entityData[i][1]
        rotatedVelocity = RotateVelocity(velocity, 45)
        entityData[i][1] = rotatedVelocity
    
    # Update the entities with the new positions and velocities
    for i, e in enumerate(entities):
        if e.GetComponent(PositionComponent) is not None:
            e.GetComponent(PositionComponent).X, e.GetComponent(PositionComponent).Y = entityData[i][0]
        if e.GetComponent(VelocityComponent) is not None:
            e.GetComponent(VelocityComponent).Vx, e.GetComponent(VelocityComponent).Vy = entityData[i][1]

    print("Simulation step completed.")

# Example usage (optional)
if __name__ == "__main__":
    # Example setup for demonstration
    width, height = 800, 600
    numEntities = 10
    entities = [Entity() for _ in range(numEntities)]
    for entity in entities:
        entity.AddComponent(PositionComponent(np.random.rand() * width, np.random.rand() * height))
        entity.AddComponent(VelocityComponent(np.random.randn() * 10, np.random.randn() * 10))