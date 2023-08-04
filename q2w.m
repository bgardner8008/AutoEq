function w = q2width(q)
%function w = q2width(q)
%
% Convert Q factor to width in octaves.
% Build a table and lookup an approximate answer.
% see width2q.m
%
maxw = 4;
minw = 0.01;
dw = 0.01;
nw = 1 + (maxw - minw) / dw;
tab = zeros(nw, 2);

for i = 0 : nw - 1
    w = minw + i * dw;
    q = width2q(w);
    tab(nw-i, 1) = w;
    tab(nw-i, 2) = q;
end

q = 1.8;
w = tab_eval_inv(tab, q)

