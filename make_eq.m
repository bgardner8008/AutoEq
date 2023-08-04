% Convert AutoEq coeffs to WA biquad filters and compute response.
% This looks correct, without factoring in the "gain" coefficient.
fs = 44100;

% these are from Senn HD 600
%(venv) E:\work\AutoEq>python -m autoeq --output-dir . --input-file "E:\work\AutoEq\measurements\headphonecom\data\over-e
%ar\Sennheiser HD 600.csv" --compensation E:\work\AutoEq\compensation\harman_over-ear_2018.csv --equalize --parametric-eq
% --parametric-eq-config "8_PEAKING_WITH_SHELVES"
gain = -6.2;
% lo shelf, hi shelf, rest are parametrics
coeffs = [105, 6.3, 0.7; ...
    10000, -6.2, 0.7; ...
    3517, -6.9, 2.12; ...
    7125, 5.0, 1.08; ...
    141, -2.4, 0.36; ...
    2047, 3.5, 1.8; ...
    493, 1.8, 0.91; ...
    4484, -2.1, 1.57; ...
    58, 1.7, 3.88; ...
    41, 0.7, 1.82];

[nr,nc] = size(coeffs);
nfilt = nr;
g = 1;
bi_arr = zeros(1, 2 * nfilt);
ai_arr = zeros(1, 2 * nfilt);
widths = zeros(nfilt, 1);

for i = 0 : nfilt-1
    fc = coeffs(i+1, 1);
    G = coeffs(i+1, 2);
    Q = coeffs(i+1, 3);
    if (i == 0)
        [b, a] = filt_ls2(fs, fc, G);
    elseif (i == 1)
        [b, a] = filt_hs2(fs, fc, G);
    else
        W = q2width(Q);
        widths(i+1) = W;
        [b, a] = filt_par(fs, fc, W, G);
    end
    [bi, ai, gi] = filt_to_biquad(b, a);
    bi_arr(i*2+1:i*2+2) = bi;
    ai_arr(i*2+1:i*2+2) = ai;
    g = g * gi;
end

for i = 1 : nfilt
    disp(sprintf('%g %g %g', coeffs(i, 1), coeffs(i, 2), widths(i)));
end

h = filter_biquad(bi_arr, ai_arr, g, impulse(16384));
figure
plotmaglogf(h);
axis([20 20000 -20 20]);

