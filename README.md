# StackSMM

#### Проект для заключительного этапа [олимпиады PROD](https://prodcontest.ru/) от команды Слоняры

## Запуск

1. Склонировать репозиторий и перейти в него:

   ```
   git clone https://github.com/Central-University-IT-prod/PROD-Slonyary.git
   cd ./PROD-Slonyary
   ```

2. Иметь установленный [Docker Engine](https://docs.docker.com/engine/)

3. Собрать и запустить:

   ```
   docker compose up -d --build
   ```

Порт бэка - **8090** \
Порт фронта - **8089**

Для локального запуска в `./frontend/src/constants.ts` замените `BACKEND_HOST` на вариант в комменатарии
