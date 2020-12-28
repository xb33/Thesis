clear
clc
%Define the global variables
global symbolTime backoffPeriod nbMax beMin beMax bos nb Wnb D PCE BOC jMax tMax lastTransmit PS PC PT PB PR Nc PZ PF PZtotal PCEtotal
%%Timing
symbolTime = 16 * 10 ^-6;
backoffPeriod = 20 * symbolTime;
%%Default MAC Parameters plus one for parameters init 0 in model
beMin = 3;
beMax = 5;
nbMax = 5;
bos = linspace(1,5,1);
nb = linspace(1,5,1);
Wnb = [8,16,32,32,32];
D = 5;
%N = 1;
% Init random values for BOC
for counter = 1 : 5
    BOC(counter) = randi([1 Wnb(counter)],1);
end
%Calculate max slots ; time
jMax = sum(Wnb(1:5));
tMax = jMax;
lastTransmit = jMax + D;
%Matrix generic state ; init each matrix
% PS = c , i , j ; c = 1 always
PS = zeros([33,5,jMax+D+1]);
PT = zeros(jMax+D,1)';
PB = zeros(jMax+D,1)';
PF = zeros(jMax+D,1)';
PR = zeros(jMax+D,1)';
PC = zeros(jMax+D,1)';
PZ = zeros(jMax+D,1)';
PZtotal = zeros(55,1)';
PCE = zeros(55,1)';
PCEtotal = zeros(55,1)';
%%Fill the matrix for the first iteration ; BOs = 1 
for Nc = 2 : 55
    %Init parameters for j = 1 as stated in the proposed algorithm
    %Nc = N;
    PB(1) = 0;
    PS(1,1,1) = 1/Wnb(1);
    for k = 2 : nbMax
        PS(1,k,1) = 0 ;
    end
    PT(1) = 0;
    PZ(1) = 0;
    PR(1) = 0;
    PC(1) = PS(1,1,1);
    for slot = 2 : jMax + D
        % The first instruction is calculate pb using (22)
        equation22(slot);
        equation2();
        equation5();
        equation8();
        equation11();
        equation14(); 
        equation16();
        equation15(slot);
        equation20(slot);
        equation21(slot);   
        equationce(slot);
    end
    PZtotal(1) = 1;
    PZtotal(Nc) = sum(PZ);
    PCEtotal(Nc) = sum(PCE);
    Pce = PZtotal + PCEtotal;
end
function pb = equation22(slot)
    %Calculate the prob busy depending on the value of D
    %if D = 1 ; equation (24) otherwise (25)
    global PB
    global D
    if D == 1
        pf = equation24(slot);
        pb = 1 - pf ;
        PB(slot) = pb;
    end
    if D > 1
        pf = equation25(slot);
        pb = 1 - pf;
        PB(slot) = pb;
    end
end
function out = equation24(slot)
    global PB
    global Nc
    global PF
    global PS
    global nbMax
    %%Call to fill the matrix sense for the actual values
    equation2();
    equation5();
    equation8();
    equation11();
    equation14();
    primero = 1 - PB(slot-1);
    acumula = 1;
    for i = 1 : nbMax
        multi = (1-PS(1,i,slot-1))^(Nc-1); 
        acumula = multi * acumula;
    end
    out = primero * acumula + PB(slot-1); 
    PF(slot) = out;
end
%%Calculate the pf for D >1
function out = equation25(slot)
    global PB
    global Nc
    global D
    global nbMax
    global PS
    global PF
    if slot > D + 1
        %%Call to fill the matrix sense for the actual values
        equation2();
        equation5();
        equation8();
        equation11();
        equation14();
        pr = ( 1 - PB(slot-1));
        mul = 1;
        for i = 1 : nbMax
            esto = ( 1 - PS(1,i,slot-1))^(Nc-1);
            mul = mul * esto;
        end
        sec = ( 1 - PB(slot-D-1));
        mu = 1 ;
        for ii = 1 : nbMax
            luk = ( 1 - PS(1,ii,slot-D-1))^(Nc-1);
            mu = mu * luk;
        end
        tird = ( 1 - mu );
        out = pr * mul + sec * tird;
        PF(slot) = out; 
    else
    primero = 1 - PB(slot-1);
    acumula = 1;
    for i = 1 : nbMax
        multi = (1-PS(1,i,slot-1))^(Nc-1); 
        acumula = multi * acumula;
    end
    out = primero * acumula ; 
    PF(slot) = out;
    end
end
%%Calculate the values for BOs = 0
function out = equation2()
    global PS
    global Wnb
    for slot = 1 : Wnb(1)
        out = 1/Wnb(1);
        PS(1,1,slot) = out;
    end
end
%%Calculate the values for BOs = 1
function out = equation5()
    global PS
    global Wnb
    global PB
    global jMax
    global D
    for slot = 1 : 2 
        out = 0;
        PS(1,2,slot) = out;
    end
    for slot = 3 : Wnb(1)+1
        suma = 0;
        for v = 2 : slot
            acumula = PS(1,1,v) * PB(v)/Wnb(1);
            suma = suma + acumula;    
        end
        out = suma;
        PS(1,2,slot) = out;
    end
    for slot = Wnb(1)+2 : Wnb(2) + 2  
        out = PS(1,2,Wnb(1));
        PS(1,2,slot) = out;
    end
    for slot = Wnb(2) + 3 : sum(Wnb(1:2))
        acumu = 0;
        for v = 2 : slot-Wnb(2)
            prim =  PS(1,1,v) * PB(v) / Wnb(1);
            acumu = prim + acumu;
        end
        primero = PS(1,2,Wnb(1));
        diferencia = primero - acumu;
        out = diferencia;
        PS(1,2,slot) = out;           
    end
    for slot = sum(Wnb(1:2)) : jMax + D 
        out = 0;
        PS(1,2,slot) = out;
    end
end
%%Calculate the values for BOS = 2
function out = equation8()
    global PB
    global PS
    global Wnb
    global jMax
    global D
    for slot = 1 : 3
        out = 0;
        PS(1,3,slot) = out;
    end
    for slot = 4 : sum(Wnb(1:2)) + 1
        suma = 0;
        for v = 3 : slot
            acumu = PS(1,2,v) * PB(v) / Wnb(3);
            suma = acumu + suma;          
        end
        PS(1,3,slot) = suma;
    end
    for slot = sum(Wnb(1:2)) + 2 : Wnb(3) + 3
        primero = PS(1,3,sum(Wnb(1:2)));
        out = primero;
        PS(1,3,slot) = out;
    end
    for slot = Wnb(3) + 4 : sum(Wnb(1:3)) 
        primero = PS(1,3,sum(Wnb(1:2)));
        suma = 0;
        for v = 3 : slot - Wnb(3)
            acumula = PS(1,2,v) * PB(v) / Wnb(3);
            suma = acumula + suma;
        end
        diferencia = primero - suma;
        out = diferencia;
        PS(1,3,slot) = out;
    end
    for slot = sum(Wnb(1:3)) : jMax + D
        PS(1,3,slot) = 0;
    end
end
%%Calculate the values for BOS = 3
function out = equation11()
    global PB
    global PS
    global Wnb
    global jMax
    global D
    for slot = 1 : 4
        out = 0;
        PS(1,4,slot) = out;
    end
    for slot = 5 : Wnb(3) + 4
        suma = 0;
        for v = 4 : slot
            acumu = PS(1,3,v) * PB(v) / Wnb(3);
            suma = acumu + suma;          
        end
        PS(1,4,slot) = suma;
    end
    for slot = Wnb(3) + 5 : sum(Wnb(1:3)) + 1
        suma = 0 ;
        suma2 = 0;
        for v = 4 : slot
            acumu = PS(1,3,v) * PB(v) / Wnb(3);
            suma = acumu + suma;
        end
        for v = 4 : slot - Wnb(3) 
            acumu2 = PS(1,3,v) * PB(v) / Wnb(3);
            suma2 = acumu2 + suma2;
        end
        diferencia = suma - suma2;
        out = diferencia;
        PS(1,4,slot) = out;
    end
    for slot = sum(Wnb(1:3)) + 2 : sum(Wnb(1:4)) 
        primero = PS(1,4,sum(Wnb(1:3)));
        suma = 0;
        for v = sum(Wnb(1:2)) : slot - Wnb(3)
            acumula = PS(1,3,v) * PB(v) / Wnb(3);
            suma = acumula + suma;
        end
        diferencia = primero - suma;
        out = diferencia;
        PS(1,4,slot) = out;
    end
    for slot = sum(Wnb(1:4)) + 1  : jMax + D
        PS(1,4,slot) = 0;
    end
end    
%%Calculate the values for BOS = 4
function out = equation14()
    global PB
    global PS
    global Wnb
    global jMax
    global D
    for slot = 1 : 5
        out = 0;
        PS(1,4,slot) = out;
    end
    for slot = 6 : Wnb(3) + 5
        suma = 0;
        for v = 5 : slot
            acumu = PS(1,3,v) * PB(v) / Wnb(3);
            suma = acumu + suma;          
        end
        PS(1,5,slot) = suma;
    end
    for slot = Wnb(3) + 6 : sum(Wnb(1:4)) + 1
        suma = 0 ;
        suma2 = 0;
        for v = 5 : slot
            acumu = PS(1,4,v) * PB(v) / Wnb(3);
            suma = acumu + suma;
        end
        for v = 5 : slot - Wnb(3) 
            acumu2 = PS(1,4,v) * PB(v) / Wnb(3);
            suma2 = acumu2 + suma2;
        end
        diferencia = suma - suma2;
        out = diferencia;
        PS(1,5,slot) = out;
    end
    for slot = sum(Wnb(1:4)) + 2 : sum(Wnb(1:5)) 
        primero = PS(1,5,sum(Wnb(1:4)));
        suma = 0;
        for v = sum(Wnb(1:3)) : slot - Wnb(3)
            acumula = PS(1,4,v) * PB(v) / Wnb(3);
            suma = acumula + suma;
        end
        diferencia = primero - suma;
        out = diferencia;
        PS(1,5,slot) = out;
    end
    for slot = sum(Wnb(1:5))+1 : jMax + D
        PS(1,5,slot) = 0;
    end
end  
%%Calculate the values for PC 
function out = equation16()
    global PS
    global nbMax
    global Wnb
    global PC
    PC(1) = PS(1,1,1);
    PC(2) = PS(1,1,2);
    for slot = 3 : 5
        suma = 0;
        for i = 1 : slot
            acum = PS(1,i,slot);
            suma = acum + suma;
        end
        out = suma;
        PC(slot) = out;
    end
    for slot = 6 : Wnb(1)
        suma = 0;
        for i = 1 : nbMax
            acum = PS(1,i,slot);
            suma = acum + suma;        
        end
        out = suma;
        PC(slot) = out;
    end
    for slot = Wnb(1) + 1 : sum(Wnb(1:2))
        suma = 0;
        for i = 2 : nbMax
            acum = PS(1,i,slot);
            suma = suma + acum;
        end
         out = suma;
         PC(slot) = out;
    end
    for slot = sum(Wnb(1:2)) + 1  : sum(Wnb(1:3))
        suma = 0;
        for i = 3 : nbMax
            acum = PS(1,i,slot);
            suma = suma + acum;            
        end
        out = suma;
        PC(slot) = out;
    end
    for slot = sum(Wnb(1:3)) + 1 : sum(Wnb(1:4))
        suma = 0;
        for i = 4 : nbMax
            acum = PS(1,i,slot);
            suma = suma + acum;
        end
        out = suma;
        PC(slot) = out;
    end
    for slot = sum(Wnb(1:4)) + 1 : sum(Wnb(1:5))
        PC(slot) = PS(1,5,slot);
    end
end
%%Calculate the values for PT
function out = equation15(slot)
    global PC
    global PB
    global D
    global PT
    if slot > D
        out = PC(slot-D) * ( 1 - PB(slot-D));
        PT(slot) = out;
    end
end
%%Calculate the probability to end tx in slot j
function out = equation20(slot)
    global PB
    global PC
    global PS
    global D
    global nbMax
    global PZ
    global Nc
    if slot > D
        first = (1 - PB(slot-D))*PC(slot-D);
        producto = 1;
        for i = 1 : nbMax
            acumula = ( 1 - PS(1,i,slot-D))^(Nc-1);
            producto = producto * acumula;
        end
        out = first * producto ;
        PZ(slot) = out;
    end
end
%%Calculate the probability the sink receives the end of the packet coming
function out = equation21(slot)
    global Nc
    global PZ
    global PR
    out = Nc * PZ(slot);
    PR(slot) = out;
end
%%Calculate the probs with CE incorporated
function out = equationce(slot)
    global PB
    global PC
    global PS
    global D
    global nbMax
    global Nc
    global PCE
    %%CE side
    Ni = 1;
    alpha = 2;
    beta = 4;
    term = (( Ni * alpha ) ^(-2/beta))/2;
    bin = nchoosek(Nc-1,Ni);
    ce = term * bin;
    %%PZ side
    if slot > D
        first = (1 - PB(slot-D))*PC(slot-D)^2;
        producto = 1;
        for i = 1 : nbMax
            acumula = ( 1 - PS(1,i,slot-D))^(Nc-2);
            producto = producto * acumula;
        end
        out = first * producto * ce ;
        PCE(slot) = out;
    end 
end


