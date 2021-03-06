# Randomized testing over a variety of types of boundary conditions.

import numpy as np
import matplotlib.pyplot as plt
import time
import pprint

from py_opt_control import min_time_bvp

decimal_places = 1

def compute_many_mp(p0, v0, a0, p1, v1, a1, params):
    """
    Compute and verify many motion primitives.
    """
    verbose = False
    start_time = time.time()
    n_mp = p0.shape[0]
    mp = []
    for i in range(n_mp):
        if verbose:
            print('Preparing to test problem data:')
            print(f"(p0, v0, a0) = {(p0[i], v0[i], a0[i])}")
            print(f"(p1, v1, a1) = {(p1[i], v1[i], a1[i])}")
        (t, j) = min_time_bvp.min_time_bvp(
        # (t, j) = min_time_bvp.min_time_bvp_paranoia(
            p0[i], v0[i], a0[i],
            p1[i], v1[i], a1[i],
            params['v_min'], params['v_max'], params['a_min'], params['a_max'], params['j_min'], params['j_max'],
            params['sync_v'], params['sync_a'], params['sync_w'])
        a, v, p = min_time_bvp.switch_states(p0[i], v0[i], a0[i], t, j)
        st, sj, sa, sv, sp = min_time_bvp.uniformly_sample(p0[i], v0[i], a0[i], t, j, dt=0.01)
        is_valid = np.allclose(p1[i], sp[:,-1]) and np.allclose(v1[i], sv[:,-1]) and np.allclose(a1[i], sa[:,-1])
        if not is_valid:
            print()
            print('Test failed. The end position is wrong. Problem data:')
            print(f"(p0, v0, a0) = {(p0[i], v0[i], a0[i])}")
            print(f"(p1, v1, a1) = {(p1[i], v1[i], a1[i])}")
            print(f"Actual final state:")
            print(f"(p, v, a) = {(sp[:,-1], sv[:,-1], sa[:,-1])}")
            print(f"Final time for each axis (should be identical):")
            print(f"{t[:,-1]}")
            print()
        mp.append({'p0':p0[i], 'v0':v0[i], 'a0':a0[i], 't':t, 'j':j, 'is_valid':is_valid})
    sec = (time.time() - start_time)/n_mp
    return mp, sec


def plot_2d_projection_many_mp(ax, mp):
    """
    Plot many motion primitives projected onto the x-y axis, independent of
    original dimension.
    """
    n_dim = mp[0]['p0'].shape[0]

    for m in mp:
        if m['is_valid']:
            st, sj, sa, sv, sp = min_time_bvp.uniformly_sample(
                m['p0'], m['v0'], m['a0'], m['t'], m['j'], dt=0.001)
            if n_dim > 1:
                ax.plot(sp[0,:], sp[1,:])
            else:
                ax.plot(sp[0,:], np.zeros_like(sp[0,:]))
    ax.axis('equal')

def test_to_zero(n_dim, params, n_tests, ax):
    p0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    v0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    a0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    p1 = np.zeros((n_tests,n_dim))
    v1 = np.zeros((n_tests,n_dim))
    a1 = np.zeros((n_tests,n_dim))
    mp, sec = compute_many_mp(p0, v0, a0, p1, v1, a1, params)
    print('\ntest_to_zero')
    n_failed = sum(1 for m in mp if not m['is_valid'])
    print(f'  failed: {n_failed/n_tests:5.1%}         ({n_failed}/{n_tests})')
    print(f'   speed:  {sec*1000:.2f} ms/test')
    plot_2d_projection_many_mp(ax, mp)
    return n_failed

def test_to_nonzero_p(n_dim, params, n_tests, ax):
    p0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    v0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    a0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    p1 = np.ones((n_tests,n_dim))
    v1 = np.zeros((n_tests,n_dim))
    a1 = np.zeros((n_tests,n_dim))
    mp, sec = compute_many_mp(p0, v0, a0, p1, v1, a1, params)
    print('\ntest_to_nonzero_p')
    n_failed = sum(1 for m in mp if not m['is_valid'])
    print(f'  failed: {n_failed/n_tests:5.1%}         ({n_failed}/{n_tests})')
    print(f'   speed:  {sec*1000:.2f} ms/test')
    plot_2d_projection_many_mp(ax, mp)
    return n_failed

def test_to_nonzero_pv(n_dim, params, n_tests, ax):
    p0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    v0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    a0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    p1 = np.ones((n_tests,n_dim))
    v1 = np.ones((n_tests,n_dim))
    v1[:,1:] = -1
    a1 = np.zeros((n_tests,n_dim))
    mp, sec = compute_many_mp(p0, v0, a0, p1, v1, a1, params)
    print('\ntest_to_nonzero_pv')
    n_failed = sum(1 for m in mp if not m['is_valid'])
    print(f'  failed: {n_failed/n_tests:5.1%}         ({n_failed}/{n_tests})')
    print(f'   speed:  {sec*1000:.2f} ms/test')
    plot_2d_projection_many_mp(ax, mp)
    return n_failed

def test_to_nonzero_a(n_dim, params, n_tests, ax):
    p0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    v0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    a0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    p1 = np.zeros((n_tests,n_dim))
    v1 = np.zeros((n_tests,n_dim))
    a1 = np.ones((n_tests,n_dim))
    a1[:,1:] = -1
    mp, sec = compute_many_mp(p0, v0, a0, p1, v1, a1, params)
    print('\ntest_to_zero')
    n_failed = sum(1 for m in mp if not m['is_valid'])
    print(f'  failed: {n_failed/n_tests:5.1%}         ({n_failed}/{n_tests})')
    print(f'   speed:  {sec*1000:.2f} ms/test')
    plot_2d_projection_many_mp(ax, mp)
    return n_failed

def test_to_nonzero_pva(n_dim, params, n_tests, ax):
    p0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    v0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    a0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    p1 = np.ones((n_tests,n_dim))
    v1 = np.ones((n_tests,n_dim))
    v1[:,1:] = -1
    a1 = -np.ones((n_tests,n_dim))
    a1[:,1:] = 1
    mp, sec = compute_many_mp(p0, v0, a0, p1, v1, a1, params)
    print('\ntest_to_nonzero_pva')
    n_failed = sum(1 for m in mp if not m['is_valid'])
    print(f'  failed: {n_failed/n_tests:5.1%}         ({n_failed}/{n_tests})')
    print(f'   speed:  {sec*1000:.2f} ms/test')
    plot_2d_projection_many_mp(ax, mp)
    return n_failed

def test_zero_a(n_dim, params, n_tests, ax):
    p0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    v0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    a0 = np.zeros((n_tests,n_dim))
    p1 = np.ones((n_tests,n_dim))
    v1 = np.ones((n_tests,n_dim))
    v1[:,1:] = -1
    a1 = np.zeros((n_tests,n_dim))
    mp, sec = compute_many_mp(p0, v0, a0, p1, v1, a1, params)
    print('\ntest_zero_a')
    n_failed = sum(1 for m in mp if not m['is_valid'])
    print(f'  failed: {n_failed/n_tests:5.1%}         ({n_failed}/{n_tests})')
    print(f'   speed:  {sec*1000:.2f} ms/test')
    plot_2d_projection_many_mp(ax, mp)
    return n_failed

def test_zero_va(n_dim, params, n_tests, ax):
    p0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    v0 = np.zeros((n_tests,n_dim))
    a0 = np.zeros((n_tests,n_dim))
    p1 = np.ones((n_tests,n_dim))
    v1 = np.zeros((n_tests,n_dim))
    a1 = np.zeros((n_tests,n_dim))
    mp, sec = compute_many_mp(p0, v0, a0, p1, v1, a1, params)
    print('\ntest_zero_va')
    n_failed = sum(1 for m in mp if not m['is_valid'])
    print(f'  failed: {n_failed/n_tests:5.1%}         ({n_failed}/{n_tests})')
    print(f'   speed:  {sec*1000:.2f} ms/test')
    plot_2d_projection_many_mp(ax, mp)
    return n_failed

def test_state_to_state(n_dim, params, n_tests, ax):
    p0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    v0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    a0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    p1 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    v1 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    a1 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    mp, sec = compute_many_mp(p0, v0, a0, p1, v1, a1, params)
    print('\ntest_state_to_state')
    n_failed = sum(1 for m in mp if not m['is_valid'])
    print(f'  failed: {n_failed/n_tests:5.1%}         ({n_failed}/{n_tests})')
    print(f'   speed:  {sec*1000:.2f} ms/test')
    plot_2d_projection_many_mp(ax, mp)
    return n_failed

def test_point_to_point(n_dim, params, n_tests, ax):
    p0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    v0 = np.zeros((n_tests,n_dim))
    a0 = np.zeros((n_tests,n_dim))
    p1 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    v1 = np.zeros((n_tests,n_dim))
    a1 = np.zeros((n_tests,n_dim))
    mp, sec = compute_many_mp(p0, v0, a0, p1, v1, a1, params)
    print('\ntest_point_to_point')
    n_failed = sum(1 for m in mp if not m['is_valid'])
    print(f'  failed: {n_failed/n_tests:5.1%}         ({n_failed}/{n_tests})')
    print(f'   speed:  {sec*1000:.2f} ms/test')
    plot_2d_projection_many_mp(ax, mp)
    return n_failed

if __name__ == '__main__':

    n_tests = 1000

    n_dim = 2

    params = {
        'v_min':  -10,
        'v_max':   10,
        'a_min':   -5,
        'a_max':    5,
        'j_min': -100,
        'j_max':  100,
        'sync_v': True,
        'sync_a': True,
        'sync_w': False,
    }

    fig, axes = plt.subplots(3, 2)
    axes = axes.flatten()

    results = {}

    n_failed = test_to_zero(n_dim, params, n_tests, axes[0])
    axes[0].set_title(f'To Zero State, Failed {n_failed}/{n_tests}')
    results['test_to_zero'] = n_failed

    n_failed = test_to_nonzero_p(n_dim, params, n_tests, axes[1])
    axes[1].set_title(f'To Nonzero P, Failed {n_failed}/{n_tests}')
    results['test_to_nonzero_p'] = n_failed

    n_failed = test_to_nonzero_a(n_dim, params, n_tests, axes[2])
    axes[2].set_title(f'To Nonzero A, Failed {n_failed}/{n_tests}')
    results['test_to_nonzero_p'] = n_failed

    n_failed = test_to_nonzero_pv(n_dim, params, n_tests, axes[3])
    axes[3].set_title(f'To Nonzero P-V, Failed {n_failed}/{n_tests}')
    results['test_to_nonzero_pv'] = n_failed

    n_failed = test_to_nonzero_pva(n_dim, params, n_tests, axes[4])
    axes[4].set_title(f'To Nonzero P-V-A, Failed {n_failed}/{n_tests}')
    results['test_to_nonzero_pva'] = n_failed

    fig, axes = plt.subplots(2, 1)
    axes = axes.flatten()

    n_failed = test_zero_va(n_dim, params, n_tests, axes[1])
    axes[1].set_title(f'Zero V-A Boundaries, Failed {n_failed}/{n_tests}')
    results['test_zero_va'] = n_failed

    n_failed = test_zero_a(n_dim, params, n_tests, axes[0])
    axes[0].set_title(f'Zero A Boundaries, Failed {n_failed}/{n_tests}')
    results['test_zero_a'] = n_failed

    fig, axes = plt.subplots(1, 2)

    n_failed = test_point_to_point(n_dim, params, n_tests, axes[0])
    axes[0].set_title(f'Point to Point, Failed {n_failed}/{n_tests}')
    results['test_point_to_point'] = n_failed

    n_failed = test_state_to_state(n_dim, params, n_tests, axes[1])
    axes[1].set_title(f'State to State, Failed {n_failed}/{n_tests}')
    results['test_state_to_state'] = n_failed

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(results)

    # Show plots.
    plt.show()
