% entry point
parse(Tokens, Result) :-
    expr(Tokens, Rest, ResTokens, _Prec),
    % accept either exact consumption or a single '$$' end marker
    ( Rest = []
    ; Rest = ['$$'] ),
    atomic_list_concat(ResTokens, ' ', Result).

% productions
% expr -> or  expr expr
% expr -> and expr expr
% expr -> not expr
% expr -> id

% Based on current(lookahead) token, decide which production to use

% or case
expr([or|T0], Rest, Res, 1) :-
    expr(T0, T1, L_toks, L_p), % parse left expr
    expr(T1, Rest0, R_toks, R_p), % parse right expr
    paren_L(L_toks, L_p, 1, L1), % add parens to left if needed
    paren_R(R_toks, R_p, 1, R1), % add parens to right if needed
    append(L1, [or|R1], Res),
    Rest = Rest0.

% and case
expr([and|T0], Rest, Res, 2) :-
    expr(T0, T1, L_toks, L_p), % parse left expr
    expr(T1, Rest0, R_toks, R_p), % parse right expr
    paren_L(L_toks, L_p, 2, L1), % add parens to left if needed
    paren_R(R_toks, R_p, 2, R1), % add parens to right if needed
    append(L1, [and|R1], Res),
    Rest = Rest0.

% not case
expr([not|T0], Rest, Res, 3) :-
    expr(T0, Rest, S_toks, S_p), % parse sub expr
    paren_un(S_toks, S_p, 3, S1), % add parens to sub expr if needed
    Res = [not|S1].

% base case: id
expr([Id|Rest], Rest, [Id], 4) :- 
    is_id(Id).

% Wrap atom in parantheses if child precedence 
% is less than parent precedence

paren_L(Toks, ChildPrec, ParentPrec, Res) :-
    ChildPrec < ParentPrec, !,
    wrap_parens(Toks, Res).
paren_L(Toks, _ChildPrec, _ParentPrec, Toks).

paren_R(Toks, ChildPrec, ParentPrec, Res) :-
    ChildPrec =< ParentPrec, !,
    wrap_parens(Toks, Res).
paren_R(Toks, _ChildPrec, _ParentPrec, Toks).

paren_un(Toks, ChildPrec, ParentPrec, Res) :-
    ChildPrec < ParentPrec, !,
    wrap_parens(Toks, Res).
paren_un(Toks, _ChildPrec, _ParentPrec, Toks).

wrap_parens(T, ['('|T2]) :-
    append(T, [')'], T2).

% checks if an atom is a valid id (a-z)
is_id(Id) :-
    atom(Id),
    atom_length(Id, 1),
    atom_chars(Id, [C]),
    member(C, [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z]).