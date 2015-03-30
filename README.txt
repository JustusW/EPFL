Installation
============

mkdir epfl_test
cd epfl_test
git clone https://github.com/JustusW/EPFL.git
git clone https://github.com/solute/pyramid_epfl.git
cd pyramid_epfl
python setup.py develop
cd ../EPFL
python setup.py develop
pserve development.ini

Das Problem
===========
Absolute Renderzeit von 2 Sekunden bei 1000 Komponenten wie im Beispiel.

Irgendwie müssen größere Mengen von Komponenten mit unterschiedlichen Basisdaten durch den Renderprozess von Jinja
laufen. Die absolute Anzahl an Templates ist mit unter 20 nicht besonders hoch, die Anzahl abweichender Aufrufe dieser
Templates ist aber in der Regel (wie im Beispiel auch) schlicht die Anzahl der unterschiedlichen Komponenten. Der
absolute Callstack steigt von ca 20 (pyramid basis) auf teilweise über 100 bei 4 Ebenen der Verschachtelung.

Zentrale Fragen wären:
Mache ich etwas offensichtliches falsch, indem ich render funktionen von externen Objekten über das Environment aufrufe
und damit rekursive Systeme ermögliche?
Gibt es Möglichkeiten diese Renderaufrufe entweder zu beschleunigen oder abzuflachen?
Ist es realistisch die genannte Menge an Daten durch die genannte Menge an Templates zu rendern?