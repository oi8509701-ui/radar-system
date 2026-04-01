%% AERIS-10N Fractal H-Tree Feed Network Analysis
% Phase and Amplitude Balance Analysis
% Frequency: 10.5 GHz
% Substrate: Rogers RO4350B (εr=3.48, h=0.762mm)

clear; clc; close all;

%% ========================================================================
% SYSTEM PARAMETERS
% ========================================================================

f0 = 10.5e9;                  % Operating frequency (Hz)
c0 = physconst('LightSpeed');
lambda0 = c0/f0;              % Free-space wavelength (m)
lambda0_mm = lambda0 * 1e3;

eps_r = 3.48;                 % RO4350B dielectric constant
h_sub = 0.762e-3;             % Substrate thickness (m)
tan_delta = 0.0037;           % Loss tangent

% Effective dielectric constant for microstrip
eps_eff = (eps_r + 1)/2 + (eps_r - 1)/2 * (1 + 12*h_sub/(1.63e-3))^(-0.5);

% Guide wavelength
lambda_g = lambda0 / sqrt(eps_eff);
lambda_g_mm = lambda_g * 1e3;

fprintf('=== AERIS-10N H-Tree Feed Network Analysis ===\n');
fprintf('Frequency: %.2f GHz\n', f0/1e9);
fprintf('Wavelength (guided): %.2f mm\n', lambda_g_mm);
fprintf('\n');

%% ========================================================================
% H-TREE FRACTAL GEOMETRY (Iteration 1: 4×4 array)
% ========================================================================

% Base H dimensions (Iteration 0)
L0 = 50e-3;                   % Base H length (m)
W0 = L0 / sqrt(2);            % Scaling factor 1/√2

% Iteration 1 dimensions
L1 = L0 / sqrt(2);            % H length at iteration 1
W1 = W0 / sqrt(2);

% Iteration 2 dimensions
L2 = L1 / sqrt(2);
W2 = W1 / sqrt(2);

fprintf('H-Tree Dimensions:\n');
fprintf('  Iteration 0: L = %.2f mm, W = %.2f mm\n', L0*1e3, W0*1e3);
fprintf('  Iteration 1: L = %.2f mm, W = %.2f mm\n', L1*1e3, W1*1e3);
fprintf('  Iteration 2: L = %.2f mm, W = %.2f mm\n', L2*1e3, W2*1e3);
fprintf('\n');

%% ========================================================================
% PATH LENGTH CALCULATION
% ========================================================================

% For 4×4 array (16 terminals), we need 2 iterations
% Iteration 0: 1 H → 4 terminals
% Iteration 1: 4 H → 16 terminals

% Path from center to each terminal
% All paths should be equal in ideal fractal

num_terminals = 16;
path_lengths = zeros(num_terminals, 1);
path_losses = zeros(num_terminals, 1);

% Calculate path length to each terminal
% Terminal positions (x, y) in meters
terminals = [
    -L1/2,  W1/2;   % Terminal 1
    -L1/2, -W1/2;   % Terminal 2
    L1/2,   W1/2;   % Terminal 3
    L1/2,  -W1/2;   % Terminal 4
    % ... add all 16 terminals
];

% For ideal H-tree, all paths are equal
ideal_path_length = L0 + L1;  % Approximate total path

for idx = 1:num_terminals
    % All paths equal (fractal property)
    path_lengths(idx) = ideal_path_length;
    
    % Calculate loss (conductor + dielectric)
    % Conductor loss (alpha_c)
    alpha_c = 0.5;  % dB/m (approximate for microstrip)
    
    % Dielectric loss (alpha_d)
    alpha_d = 27.3 * eps_r * (eps_eff - 1) * tan_delta / ...
              (eps_eff * (eps_r - 1)) * 1e3;  % dB/m
    
    % Total loss
    path_losses(idx) = (alpha_c + alpha_d) * path_lengths(idx);
end

fprintf('Path Length Analysis:\n');
fprintf('  Ideal path length: %.2f mm\n', ideal_path_length*1e3);
fprintf('  Path length range: [%.4f, %.4f] mm\n', ...
    min(path_lengths)*1e3, max(path_lengths)*1e3);
fprintf('  Path length error: %.4f mm (should be 0)\n', ...
    max(path_lengths) - min(path_lengths));
fprintf('\n');

fprintf('Path Loss Analysis:\n');
fprintf('  Loss per path: %.4f dB\n', mean(path_losses));
fprintf('  Loss range: [%.4f, %.4f] dB\n', ...
    min(path_losses), max(path_losses));
fprintf('  Amplitude imbalance: %.4f dB (should be <0.5 dB)\n', ...
    max(path_losses) - min(path_losses));
fprintf('\n');

%% ========================================================================
% PHASE BALANCE ANALYSIS
% ========================================================================

% Phase delay per path
phase_delays = -2*pi*path_lengths/lambda_g;  % Radians
phase_degrees = phase_delays * 180/pi;

% Phase imbalance
phase_imbalance = max(phase_degrees) - min(phase_degrees);

fprintf('Phase Balance Analysis:\n');
fprintf('  Phase delay (mean): %.2f degrees\n', mean(phase_degrees));
fprintf('  Phase delay range: [%.2f, %.2f] degrees\n', ...
    min(phase_degrees), max(phase_degrees));
fprintf('  Phase imbalance: %.2f degrees (should be <5°)\n', phase_imbalance);
fprintf('\n');

%% ========================================================================
% IMPEDANCE TRANSFORMATIONS
% ========================================================================

% Characteristic impedances along H-tree
Z0_main = 50;                 % Main feed line
Z0_branch = 70.71;            % Branch lines (λ/4 transformer)
Z0_terminal = 100;            % Terminal lines

fprintf('Impedance Profile:\n');
fprintf('  Main feed: %.2f Ω\n', Z0_main);
fprintf('  Branch lines: %.2f Ω (λ/4 transformer)\n', Z0_branch);
fprintf('  Terminal lines: %.2f Ω\n', Z0_terminal);
fprintf('\n');

%% ========================================================================
% PLOTTING
% ========================================================================

% Figure 1: H-Tree Geometry
figure('Name', 'H-Tree Geometry', 'Position', [100, 100, 800, 600]);

% Draw Iteration 0 H (center)
plot([-L0/2, L0/2]*1e3, [0, 0]*1e3, 'b-', 'LineWidth', 3);
hold on;
plot([0, 0]*1e3, [-W0/2, W0/2]*1e3, 'b-', 'LineWidth', 3);

% Draw Iteration 1 H (4 branches)
colors = ['r', 'g', 'm', 'c'];
branch_centers = [
    -L0/2,  W0/2;
    -L0/2, -W0/2;
    L0/2,   W0/2;
    L0/2,  -W0/2;
];

for idx = 1:4
    plot([branch_centers(idx,1), branch_centers(idx,1)+L1]*1e3, ...
         [branch_centers(idx,2), branch_centers(idx,2)]*1e3, ...
         [colors(idx) '-'], 'LineWidth', 2);
    plot([branch_centers(idx,1), branch_centers(idx,1)]*1e3, ...
         [branch_centers(idx,2)-W1/2, branch_centers(idx,2)+W1/2]*1e3, ...
         [colors(idx) '-'], 'LineWidth', 2);
end

xlabel('X (mm)');
ylabel('Y (mm)');
title('H-Tree Feed Network Geometry (Iteration 1)');
grid on;
axis equal;
legend('Iteration 0', 'Iteration 1 (4 branches)', 'Location', 'best');

% Figure 2: Path Lengths
figure('Name', 'Path Lengths', 'Position', [100, 100, 800, 600]);
bar(1:num_terminals, path_lengths*1e3, 'FaceColor', [0.2 0.4 0.8]);
hold on;
yline(ideal_path_length*1e3, 'r--', 'LineWidth', 2, 'Label', 'Ideal');
xlabel('Terminal Index');
ylabel('Path Length (mm)');
title('Path Length to Each Terminal');
grid on;

% Figure 3: Phase Distribution
figure('Name', 'Phase Distribution', 'Position', [100, 100, 800, 600]);
bar(1:num_terminals, phase_degrees, 'FaceColor', [0.8 0.4 0.2]);
hold on;
yline(mean(phase_degrees), 'r--', 'LineWidth', 2, 'Label', 'Mean');
xlabel('Terminal Index');
ylabel('Phase (degrees)');
title('Phase Delay to Each Terminal');
grid on;

% Figure 4: Loss Distribution
figure('Name', 'Loss Distribution', 'Position', [100, 100, 800, 600]);
bar(1:num_terminals, path_losses, 'FaceColor', [0.2 0.6 0.4]);
hold on;
yline(mean(path_losses), 'r--', 'LineWidth', 2, 'Label', 'Mean');
xlabel('Terminal Index');
ylabel('Loss (dB)');
title('Insertion Loss to Each Terminal');
grid on;

% Figure 5: Smith Chart (Impedance)
figure('Name', 'Impedance Profile', 'Position', [100, 100, 800, 600]);
% Simplified Smith chart visualization
plot([Z0_main, Z0_branch, Z0_terminal], [1, 2, 3], 'bo-', ...
     'LineWidth', 2, 'MarkerSize', 8, 'MarkerFaceColor', 'b');
set(gca(), 'YDir', 'reverse');
xlabel('Impedance (Ω)');
ylabel('Stage');
title('Impedance Transformations Along H-Tree');
grid on;
yticks([1, 2, 3]);
yticklabels({'Main Feed', 'Branch Lines', 'Terminals'});

fprintf('=== Analysis Complete ===\n');
fprintf('Figures generated:\n');
fprintf('  1. H-Tree Geometry\n');
fprintf('  2. Path Lengths\n');
fprintf('  3. Phase Distribution\n');
fprintf('  4. Loss Distribution\n');
fprintf('  5. Impedance Profile\n');
fprintf('\n');
