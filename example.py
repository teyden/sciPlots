from scipy.integrate import ode

y0, t0 = [1.0j, 2.0], 0

def f(t, y, arg1):
    return [1j*arg1*y[0] + y[1], -arg1*y[1]**2]
def jac(t, y, arg1):
    return [[1j*arg1, 1], [0, -arg1*2*y[1]]]


r = ode(f, jac).set_integrator('zvode', method='bdf', with_jacobian=True)
r.set_initial_value(y0, t0).set_f_params(2.0).set_jac_params(2.0)
t1 = 10
dt = 1
while r.successful() and r.t < t1:
    r.integrate(r.t+dt)
    print("%s %s" % (r.t, r.y))