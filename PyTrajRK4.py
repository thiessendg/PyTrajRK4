import math

G = -9.80665    # gravitational constant at earth surface m/s/s
re = 6371000.0  # mean radius of earth in m


class Projectile:
    verticalPosition = 0
    verticalVelocity = 0
    verticalAcceleration = 0

    horizontalPosition = 0
    horizontalVelocity = 0
    horizontalAcceleration = 0


def rk4(state, dt):
    """Returns final (position, velocity) tuple after
        time dt has passed.
        ypos: initial position (number-like object)
        yvel: initial velocity (number-like object)
        yaccel: acceleration function a(x,v,dt) (must be callable)
        xpos: initial position (number-like object)
        xvel: initial velocity (number-like object)
        xaccel: acceleration function a(x,v,dt) (must be callable)
        dt: timestep (number)
        :param dt: timestep (number)
        :param state: Projectile (object)"""

    # kp1y = projectile.vertPos
    kv1y = state.verticalVelocity
    ka1y = state.verticalAcceleration

    kp2y = state.verticalPosition + 0.5 * kv1y * dt
    kv2y = state.verticalVelocity + 0.5 * ka1y * dt
    ka2y = yAcceleration(kp2y)

    kp3y = state.verticalPosition + 0.5 * kv2y * dt
    kv3y = state.verticalVelocity + 0.5 * ka2y * dt
    ka3y = yAcceleration(kp3y)

    kp4y = state.verticalPosition + kv3y * dt
    kv4y = state.verticalVelocity + ka3y * dt
    ka4y = yAcceleration(kp4y)

    # kp1x = xpos
    kv1x = state.horizontalVelocity
    ka1x = state.horizontalAcceleration

    # kp2x = xpos + 1/2 * kv1x * dt
    kv2x = state.horizontalVelocity + 0.5 * ka1x * dt
    ka2x = xAcceleration()

    # kp3x = xpos + 1/2 * kv2x * dt
    kv3x = state.horizontalVelocity + 0.5 * ka2x * dt
    ka3x = xAcceleration()

    # kp4x = xpos + kv3x * dt
    kv4x = state.horizontalVelocity + ka3x * dt
    ka4x = xAcceleration()

    state.verticalPosition += (dt / 6) * (kv1y + 2 * (kv2y + kv3y) + kv4y)
    state.verticalVelocity += (dt / 6) * (ka1y + 2 * (ka2y + ka3y) + ka4y)
    state.verticalAcceleration = yAcceleration(state.verticalPosition)

    state.horizontalPosition += (dt / 6) * (kv1x + 2 * (kv2x + kv3x) + kv4x)
    state.horizontalVelocity += (dt / 6) * (ka1x + 2 * (ka2x + ka3x) + ka4x)
    state.horizontalAcceleration = xAcceleration()

    return state


def yAcceleration(h):
    """Determines acceleration from current position,
        velocity, and timestep. This particular acceleration
        function models a spring.
        h: altitude (number-like object)
        :param h: """
    #  stiffness = 1
    #  damping = -0.005
    #  return -stiffness*x - damping*v
    return G * (re / (re + h)) * (re / (re + h))


def xAcceleration():
    """Determines acceleration from current position,
        velocity, and timestep. This particular acceleration
        function models a spring."""
    #  stiffness = 1
    #  damping = -0.005
    #  return -stiffness*x - damping*v
    return 0

height = float(input("Enter initial elevation/height (m): \n"))

theta = float(input("Enter firing angle (0-90 (degrees)): \n"))
while (theta < 0 or theta > 90):
    theta = float(input("ERROR\nEnter firing angle between 0-90 degrees): \n"))

theta *= math.pi / 180

initialVelocity = float(input("Enter initial velocity (m/s): \n"))
while (initialVelocity < 0):
    initialVelocity = float(input("ERROR\nEnter a non negative initial velocity (m/s): \n"))
    
deltaTime = float(input("Enter the time step (s) per integration: \n"))
while (deltaTime < 0):
    deltaTime = float(input("ERROR\nEnter a non negative time step (s) per integration: \n"))

duration = float(input("Enter final time (s): \n"))
while (duration < 0):
    duration = float(input("ERROR\n Enter a non negative final time (s): \n"))
    
projectile = Projectile
projectile.verticalPosition = height
projectile.verticalVelocity = initialVelocity * math.sin(theta)
projectile.verticalAcceleration = yAcceleration(projectile.verticalPosition)
projectile.horizontalPosition = 0
projectile.horizontalVelocity = initialVelocity * math.cos(theta)
projectile.horizontalAcceleration = xAcceleration()

currentTimeElapsed = 0

while (currentTimeElapsed <= duration) and (projectile.verticalPosition >= 0):
    projectile = rk4(projectile, deltaTime)
    #  Integrate using Euler's method
    #  euler = (
    #        euler[0] + euler[1]*dt,
    #        euler[1] + accel(euler[0],euler[1],dt)*dt
    #        )
    currentTimeElapsed += deltaTime
    #if (currentTimeElapsed <= duration) and (projectile.verticalPosition >= 0):
    print("t = %.5f" % currentTimeElapsed)
    print("     y = %.9f y' = %.9f y'' = %.9f" % 
              (projectile.verticalPosition, projectile.verticalVelocity, projectile.verticalAcceleration))
    print("     x = %.9f x' = %.9f x'' = %.9f" % 
              (projectile.horizontalPosition, projectile.horizontalVelocity, projectile.horizontalAcceleration))