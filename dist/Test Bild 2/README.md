
# Shooter game
###### QuantumGame project

![icon](presets/ShooterGame_Ico.png)

##### Мини - описание
мини игрушка - шутер, обычное управление
* `WASD` - движение
* `L-CL` - стрельба
* `R` - перезарядка
* `Enter/7 кнопка мыши`- взвести оружие
* `Esc` - выход
Реализованно управление с геймпада, оно тоже обычное, на 2 аксиса, курок и перекрестие

реализованные аспекты:
1) XP - жизнь у бочек
2) weapons
3) управление с геймпада
4) перезарядка оружия в 2 этапа
5) подбор с пола

В планах:
1) разнообразие в типах оружия (частично реализовано)
2) игра в онлайне
3) декорации и несложная физика

##### Команда на компиляцию в консоль
* с помощью pyinstaller:
```shell
pyinstaller --name "Test Bild" --icon="Engine/data/ico.ico" --add-data "C:/Program Files/Python311/Lib/site-packages/glcontext;glcontext" --add-data "C:/Program Files/Python311/Lib/site-packages/toml;toml" --add-data "Engine/data;Engine/data"  --add-data "presets;presets" main.py
```
