FROM python:3.6

WORKDIR /usr/src/app

COPY . .

RUN pip install --force-reinstall pip==9.0.3
RUN pip install --no-cache-dir -r requirements.txt

ENV DEBUG yes

ENV BERNARD_SETTINGS_FILE /usr/src/app/src/wadrid/settings.py
ENV FRAMEX_API_URL https://framex-dev.wadrid.net/api/

CMD [ "python", "./manage.py", "run" ]

EXPOSE 8666