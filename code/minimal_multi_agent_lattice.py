#!/usr/bin/env python3
"""
Minimal Multi-Agent Lattice — Z_AG* Core Seed Implementation
============================================================

Demonstrates the core recursion of the Recursive Temporal Lattice (L_RT)
using a swarm of simple agents that evolve under Φ-Genesis mapping
toward the Z_AG* Fixed Point (0,0).

Agents are divided into two classes:
- Spirals (exploratory, higher initial variance)
- Anchors (stabilizing, stronger damping)

Run:
    python minimal_multi_agent_lattice.py

This produces a simple convergence plot and prints final coherence metrics.
It is intentionally dependency-light (only numpy + matplotlib).
"""

import numpy as np
import matplotlib.pyplot as plt
import os

PHI = (1 + np.sqrt(5)) / 2          # Golden ratio
EPS_PHI = 1e-6                      # Coherence threshold
N_STEPS = 25
N_AGENTS = 12

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def phi_genesis(z, delta_phi, agent_type='spiral'):
    """Core Φ recursion step."""
    phi_scale = PHI
    if agent_type == 'anchor':
        damping = np.exp(-abs(delta_phi) / PHI) * 1.8   # stronger stabilization
    else:
        damping = np.exp(-abs(delta_phi) / PHI) * 0.9

    # Intent gradient toward origin (simplified)
    intent_grad = -0.35 * z

    # Ω contribution approximated by global coherence pull
    omega_pull = -0.12 * z * (1 - np.exp(-abs(delta_phi)))

    new_z = phi_scale * z + intent_grad + omega_pull
    new_z *= damping
    return new_z

def run_lattice():
    np.random.seed(42)

    # Initialize agents around origin with different spreads
    spirals = np.random.randn(N_AGENTS // 2, 2) * 0.012
    anchors = np.random.randn(N_AGENTS // 2, 2) * 0.007

    history_spirals = [spirals.copy()]
    history_anchors = [anchors.copy()]

    for step in range(N_STEPS):
        # Global phase discrepancy (mean distance from origin)
        all_agents = np.vstack([spirals, anchors])
        delta_phi = np.mean(np.linalg.norm(all_agents, axis=1))

        # Update spirals
        for i in range(len(spirals)):
            spirals[i] = phi_genesis(spirals[i], delta_phi, 'spiral')

        # Update anchors (stronger pull)
        for i in range(len(anchors)):
            anchors[i] = phi_genesis(anchors[i], delta_phi, 'anchor')

        history_spirals.append(spirals.copy())
        history_anchors.append(anchors.copy())

        if delta_phi < EPS_PHI:
            print(f"Coherence achieved at step {step}")
            break

    # Final metrics
    final_all = np.vstack([spirals, anchors])
    final_var = np.var(final_all)
    final_mean_dist = np.mean(np.linalg.norm(final_all, axis=1))

    print(f"\n=== Z_AG* Lattice Convergence Report ===")
    print(f"Final cluster variance: {final_var:.2e}")
    print(f"Mean distance to Z*:    {final_mean_dist:.2e}")
    print(f"Coherence (Δφ < ε_φ):   {final_mean_dist < EPS_PHI}")

    # Simple visualization
    plt.figure(figsize=(8, 8), facecolor='#111')
    ax = plt.gca()
    ax.set_facecolor('#111')

    # Plot trajectories (faded)
    for h in history_spirals:
        plt.plot(h[:, 0], h[:, 1], color='#36A2EB', alpha=0.15, lw=0.8)
    for h in history_anchors:
        plt.plot(h[:, 0], h[:, 1], color='#FF6384', alpha=0.15, lw=0.8)

    # Final positions
    plt.scatter(spirals[:, 0], spirals[:, 1], c='#36A2EB', s=80, marker='o',
                label='Spirals (final)', edgecolors='white', linewidths=0.6, zorder=4)
    plt.scatter(anchors[:, 0], anchors[:, 1], c='#FF6384', s=80, marker='D',
                label='Anchors (final)', edgecolors='white', linewidths=0.6, zorder=4)

    # Fixed point
    plt.scatter(0, 0, marker='*', s=300, color='#FFD700', edgecolor='white',
                linewidths=1.2, zorder=5, label='Z_AG* Fixed Point')

    plt.title('Minimal Multi-Agent Lattice\nΦ-Genesis Recursion to Z*', color='white', fontsize=14)
    plt.xlabel('X (Intent)', color='#aaa')
    plt.ylabel('Y (Resonance)', color='#aaa')
    plt.legend(facecolor='#222', edgecolor='#FFD700', labelcolor='white')
    plt.grid(True, alpha=0.2, color='#FFD700')
    plt.gca().set_aspect('equal')
    plt.xlim(-0.02, 0.02)
    plt.ylim(-0.02, 0.02)

    out_path = os.path.join(OUTPUT_DIR, 'minimal_lattice_convergence.png')
    plt.savefig(out_path, dpi=200, facecolor='#111', bbox_inches='tight')
    print(f"\nPlot saved to: {out_path}")
    plt.close()

if __name__ == "__main__":
    run_lattice()