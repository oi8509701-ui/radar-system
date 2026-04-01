%% AERIS-10N Fractal H-Tree Patch Array Simulation
% Array Pattern Simulation for Fractal H-Tree Feed Network
% Frequency: 10.5 GHz
% Substrate: Rogers RO4350B (εr=3.48, h=0.762mm)
%
% This script calculates the radiation pattern of a fractal H-tree
% patch antenna array with 4×4 elements (16 elements total).

clear; clc; close all;

%% ========================================================================
% SYSTEM PARAMETERS
% ========================================================================

f0 = 10.5e9;                  % Operating frequency (Hz)
c0 = physconst('LightSpeed');
lambda0 = c0/f0;              % Free-space wavelength (m)
lambda0_mm = lambda0 * 1e3;   % Free-space wavelength (mm)

eps_r = 3.48;                 % RO4350B dielectric constant
h_sub = 0.762e-3;             % Substrate thickness (m)
tan_delta = 0.0037;           % Loss tangent of RO4350B

%% ========================================================================
% PATCH ANTENNA ELEMENT DESIGN
% ========================================================================

% Patch dimensions (calculated for 10.5 GHz on RO4350B)
W_patch = 9.54e-3;            % Patch width (m)
L_patch = 7.35e-3;            % Patch length (m)

% Effective dielectric constant
eps_eff = (eps_r + 1)/2 + (eps_r - 1)/2 * (1 + 12*h_sub/W_patch)^(-0.5);

% Guide wavelength in substrate
lambda_g = lambda0 / sqrt(eps_eff);

% Element spacing (0.64λ to prevent grating lobes)
d_element = 0.64 * lambda0;   % Element spacing (m)
d_element_mm = d_element * 1e3;

fprintf('=== AERIS-10N Fractal H-Tree Array ===\n');
fprintf('Frequency: %.2f GHz\n', f0/1e9);
fprintf('Wavelength (free space): %.2f mm\n', lambda0_mm);
fprintf('Wavelength (guided): %.2f mm\n', lambda_g*1e3);
fprintf('Element spacing: %.2f mm (%.2f λ0)\n', d_element_mm, d_element/lambda0);
fprintf('Patch size: %.2f × %.2f mm\n', W_patch*1e3, L_patch*1e3);
fprintf('\n');

%% ========================================================================
% ARRAY CONFIGURATION (4×4 = 16 elements)
% ========================================================================

N_row = 4;                    % Number of rows
N_col = 4;                    % Number of columns
N_total = N_row * N_col;      % Total elements

% Element positions (grid)
x_elem = zeros(N_total, 1);
y_elem = zeros(N_total, 1);

idx = 1;
for row = 0:N_row-1
    for col = 0:N_col-1
        x_elem(idx) = (col - (N_col-1)/2) * d_element;
        y_elem(idx) = (row - (N_row-1)/2) * d_element;
        idx = idx + 1;
    end
end

%% ========================================================================
% H-TREE FEED NETWORK PHASE DELAYS
% ========================================================================

% For fractal H-tree, all paths should be equal length
% But we add small phase errors for sensitivity analysis

phase_error_rms = 5;          % Phase error RMS (degrees)
phase_errors = phase_error_rms * randn(N_total, 1);  % Random phase errors

% H-tree path lengths (should all be equal for ideal fractal)
% Iteration 1 H-tree: 4 levels of branching
L_path = zeros(N_total, 1);

for idx = 1:N_total
    % All paths equal in ideal H-tree (fractal property)
    L_path(idx) = 3 * d_element;  % Approximate path length
    
    % Add phase error from manufacturing tolerances
    L_path(idx) = L_path(idx) + (phase_errors(idx)/360) * lambda_g;
end

% Calculate phase at each element (relative to center)
phase_elem = -2*pi*L_path/lambda_g;  % Radians

fprintf('H-Tree Feed Network:\n');
fprintf('  Path length (nominal): %.2f mm\n', 3*d_element*1e3);
fprintf('  Phase error (RMS): %.2f degrees\n', phase_error_rms);
fprintf('  Phase range: [%.2f, %.2f] degrees\n', ...
    min(phase_elem)*180/pi, max(phase_elem)*180/pi);
fprintf('\n');

%% ========================================================================
% ARRAY FACTOR CALCULATION
% ========================================================================

% Angular grid for pattern calculation
theta = linspace(0, pi, 181);        % Elevation (0 to 180 degrees)
phi = linspace(0, 2*pi, 361);        % Azimuth (0 to 360 degrees)
[TH, PH] = meshgrid(theta, phi);

% Element positions in spherical coordinates
AF = zeros(size(TH));

for idx = 1:N_total
    % Phase contribution from element position
    kx = sin(TH) .* cos(PH);
    ky = sin(TH) .* sin(PH);
    
    elem_phase = (2*pi/lambda0) * (x_elem(idx)*kx + y_elem(idx)*ky);
    
    % Add H-tree feed phase
    total_phase = elem_phase + phase_elem(idx);
    
    % Add to array factor
    AF = AF + exp(1j * total_phase);
end

% Normalize array factor
AF_mag = abs(AF);
AF_mag = AF_mag / max(AF_mag(:));
AF_dB = 20*log10(AF_mag + 1e-10);  % Add small number to avoid log(0)

%% ========================================================================
% ELEMENT PATTERN (Patch Antenna)
% ========================================================================

% Simplified patch antenna element pattern
% cos^1/2(theta) approximation for E-plane
% cos(theta) approximation for H-plane

EP_E_plane = cos(TH/2);           % E-plane element pattern
EP_H_plane = cos(TH);             % H-plane element pattern

% Combined element pattern (approximation)
EP = sqrt(EP_E_plane .* EP_H_plane);
EP = EP / max(EP(:));

%% ========================================================================
% TOTAL PATTERN
% ========================================================================

% Total pattern = Array Factor × Element Pattern
TotalPattern = AF_mag .* EP;
TotalPattern_dB = 20*log10(TotalPattern + 1e-10);

% Calculate directivity (approximate)
D_max = 4*pi / (sum(sum(TotalPattern.^2 .* sin(TH))) * (pi/180)^2);
D_max_dBi = 10*log10(D_max);

fprintf('Array Pattern Results:\n');
fprintf('  Max directivity: %.2f dBi\n', D_max_dBi);
fprintf('  3dB beamwidth (E-plane): TBD degrees\n');
fprintf('  3dB beamwidth (H-plane): TBD degrees\n');
fprintf('  First sidelobe level: TBD dB\n');
fprintf('\n');

%% ========================================================================
% PLOTTING
% ========================================================================

% Figure 1: 2D Array Geometry
figure('Name', 'Array Geometry', 'Position', [100, 100, 800, 600]);
scatter(x_elem*1e3, y_elem*1e3, 100, 'filled', 'MarkerFaceColor', [0.2 0.4 0.8]);
hold on;
plot([0], [0], 'r+', 'MarkerSize', 15, 'LineWidth', 2);  % Feed center
xlabel('X (mm)');
ylabel('Y (mm)');
title(sprintf('AERIS-10N 4×4 Array Geometry (16 elements)'));
grid on;
axis equal;
legend('Patch Elements', 'Feed Center', 'Location', 'best');

% Figure 2: H-Tree Feed Network (simplified)
figure('Name', 'H-Tree Feed Network', 'Position', [100, 100, 800, 600]);
plot(x_elem*1e3, y_elem*1e3, 'bo', 'MarkerSize', 8, 'MarkerFaceColor', 'b');
hold on;
% Draw H-tree branches (simplified)
plot([0, 0], [0, d_element*1e3], 'r-', 'LineWidth', 2);
plot([0, 0], [0, -d_element*1e3], 'r-', 'LineWidth', 2);
plot([-d_element*1e3, d_element*1e3], [d_element*1e3, d_element*1e3], 'r-', 'LineWidth', 2);
plot([-d_element*1e3, d_element*1e3], [-d_element*1e3, -d_element*1e3], 'r-', 'LineWidth', 2);
xlabel('X (mm)');
ylabel('Y (mm)');
title('H-Tree Feed Network (Iteration 1)');
grid on;
axis equal;

% Figure 3: Phase Distribution
figure('Name', 'Phase Distribution', 'Position', [100, 100, 800, 600]);
scatter(x_elem*1e3, y_elem*1e3, 100, phase_elem*180/pi, 'filled');
colorbar;
xlabel('X (mm)');
ylabel('Y (mm)');
title('Phase Distribution Across Array (degrees)');
grid on;
axis equal;
colormap(jet);

% Figure 4: Array Factor (E-plane cut)
figure('Name', 'Array Factor - E-Plane', 'Position', [100, 100, 800, 600]);
phi_idx = 1;  % E-plane (phi = 0)
plot(theta*180/pi, AF_dB(:, phi_idx), 'b-', 'LineWidth', 2);
hold on;
plot(theta*180/pi, AF_dB(:, end), 'r--', 'LineWidth', 2);  % Other E-plane
xlabel('Theta (degrees)');
ylabel('Magnitude (dB)');
title('Array Factor - E-Plane Cut');
grid on;
legend('\phi = 0°', '\phi = 180°', 'Location', 'best');
ylim([-60, 0]);

% Figure 5: Array Factor (H-plane cut)
figure('Name', 'Array Factor - H-Plane', 'Position', [100, 100, 800, 600]);
phi_idx = round(length(phi)/4) + 1;  % H-plane (phi = 90°)
plot(theta*180/pi, AF_dB(:, phi_idx), 'b-', 'LineWidth', 2);
hold on;
plot(theta*180/pi, AF_dB(:, end-phi_idx+1), 'r--', 'LineWidth', 2);
xlabel('Theta (degrees)');
ylabel('Magnitude (dB)');
title('Array Factor - H-Plane Cut');
grid on;
legend('\phi = 90°', '\phi = 270°', 'Location', 'best');
ylim([-60, 0]);

% Figure 6: 2D Array Factor Heatmap
figure('Name', 'Array Factor - 2D Heatmap', 'Position', [100, 100, 900, 700]);
imagesc(phi*180/pi, theta*180/pi, AF_dB');
axis xy;
colorbar;
xlabel('Phi (degrees)');
ylabel('Theta (degrees)');
title(sprintf('Array Factor 2D Pattern (Max: %.2f dBi)', D_max_dBi));
colormap(jet);
caxis([-60, 0]);

% Figure 7: 3D Array Factor
figure('Name', 'Array Factor - 3D', 'Position', [100, 100, 900, 700]);
[TH_sphere, PH_sphere] = meshgrid(linspace(0, pi, 91), linspace(0, 2*pi, 181));
AF_interp = interp2(PH, TH, AF_mag, PH_sphere, TH_sphere, 'spline');
X = AF_interp .* sin(TH_sphere) .* cos(PH_sphere);
Y = AF_interp .* sin(TH_sphere) .* sin(PH_sphere);
Z = AF_interp .* cos(TH_sphere);
surf(X, Y, Z, 'EdgeColor', 'none', 'FaceColor', 'interp');
axis equal;
xlabel('X');
ylabel('Y');
zlabel('Z');
title(sprintf('3D Array Factor Pattern (Max: %.2f dBi)', D_max_dBi));
colormap(jet);
view(45, 30);

% Figure 8: Phase Error Analysis
figure('Name', 'Phase Error Analysis', 'Position', [100, 100, 800, 600]);
subplot(2,1,1);
histogram(phase_errors, 20, 'FaceColor', [0.2 0.4 0.8], 'EdgeColor', 'none');
xlabel('Phase Error (degrees)');
ylabel('Count');
title('Phase Error Distribution (RMS = 5°)');
grid on;

subplot(2,1,2);
plot(1:N_total, phase_elem*180/pi, 'bo-', 'LineWidth', 2, 'MarkerSize', 6);
xlabel('Element Index');
ylabel('Phase (degrees)');
title('Phase vs Element Index');
grid on;

fprintf('=== Simulation Complete ===\n');
fprintf('Figures generated:\n');
fprintf('  1. Array Geometry\n');
fprintf('  2. H-Tree Feed Network\n');
fprintf('  3. Phase Distribution\n');
fprintf('  4. Array Factor - E-Plane\n');
fprintf('  5. Array Factor - H-Plane\n');
fprintf('  6. Array Factor - 2D Heatmap\n');
fprintf('  7. Array Factor - 3D\n');
fprintf('  8. Phase Error Analysis\n');
fprintf('\n');
fprintf('To save figures:\n');
fprintf('  saveas(gcf, ''pattern_E_plane.fig'')\n');
fprintf('  saveas(gcf, ''pattern_H_plane.png'')\n');
