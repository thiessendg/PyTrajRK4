import math

g = -9.80665    # gravitational constant at earth surface m/s/s
re = 6371000.0  # mean radius of earth in m


class Projectile:
    vertPos = 0
    vertVel = 0
    vertAcc = 0

    horzPos = 0
    horzVel = 0
    horzAcc = 0


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
    kv1y = state.vertVel
    ka1y = state.vertAcc

    kp2y = state.vertPos + 0.5 * kv1y * dt
    kv2y = state.vertVel + 0.5 * ka1y * dt
    ka2y = yaccel(kp2y)

    kp3y = state.vertPos + 0.5 * kv2y * dt
    kv3y = state.vertVel + 0.5 * ka2y * dt
    ka3y = yaccel(kp3y)

    kp4y = state.vertPos + kv3y * dt
    kv4y = state.vertVel + ka3y * dt
    ka4y = yaccel(kp4y)

    # kp1x = xpos
    kv1x = state.horzVel
    ka1x = state.horzAcc

    # kp2x = xpos + 1/2 * kv1x * dt
    kv2x = state.horzVel + 0.5 * ka1x * dt
    ka2x = xaccel()

    # kp3x = xpos + 1/2 * kv2x * dt
    kv3x = state.horzVel + 0.5 * ka2x * dt
    ka3x = xaccel()

    # kp4x = xpos + kv3x * dt
    kv4x = state.horzVel + ka3x * dt
    ka4x = xaccel()

    state.vertPos += (dt / 6) * (kv1y + 2 * (kv2y + kv3y) + kv4y)
    state.vertVel += (dt / 6) * (ka1y + 2 * (ka2y + ka3y) + ka4y)
    state.vertAcc = yaccel(state.vertPos)

    state.horzPos += (dt / 6) * (kv1x + 2 * (kv2x + kv3x) + kv4x)
    state.horzVel += (dt / 6) * (ka1x + 2 * (ka2x + ka3x) + ka4x)
    state.horzAcc = xaccel()

    return state


def yaccel(h):
    """Determines acceleration from current position,
        velocity, and timestep. This particular acceleration
        function models a spring.
        h: altitude (number-like object)
        :param h: """
    #  stiffness = 1
    #  damping = -0.005
    #  return -stiffness*x - damping*v
    return g * (re / (re + h)) * (re / (re + h))


def xaccel():
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

v0 = float(input("Enter initial velocity (m/s): \n"))
while (v0 < 0):
    v0 = float(input("ERROR\nEnter a non negative initial velocity (m/s): \n"))
    
deltat = float(input("Enter the time step (s) per integration: \n"))
while (deltat < 0):
    deltat = float(input("ERROR\nEnter a non negative time step (s) per integration: \n"))

duration = float(input("Enter final time (s): \n"))
while (duration < 0):
    duration = float(input("ERROR\n Enter a non negative final time (s): \n"))
    
projectile = Projectile
projectile.vertPos = height
projectile.vertVel = v0 * math.sin(theta)
projectile.vertAcc = yaccel(projectile.vertPos)
projectile.horzPos = 0
projectile.horzVel = v0 * math.cos(theta)
projectile.horzAcc = xaccel()

t = 0

while (t < duration) and (projectile.vertPos >= 0):
    projectile = rk4(projectile, deltat)
    #  Integrate using Euler's method
    #  euler = (
    #        euler[0] + euler[1]*dt,
    #        euler[1] + accel(euler[0],euler[1],dt)*dt
    #        )
    t += deltat
    if (t < duration) and (projectile.vertPos >= 0):
        print("t=%.5f" % t)
        print("     y=%.9f y'=%.9f y''=%.9f" % 
              (projectile.vertPos, projectile.vertVel, projectile.vertAcc))
        print("     x=%.9f x'=%.9f x''=%.9f" % 
              (projectile.horzPos, projectile.horzVel, projectile.horzAcc))