SCRIPTS := applications/init-scripts/scripts
SETTINGS := app.settings.local

FLUSH := flush --settings=$(SETTINGS) --noinput
DJANGO_EXEC=docker-compose run --rm web python manage.py
PYTHON_EXEC=docker-compose run --rm web python

LOADDATA := $(SCRIPTS)/import_initial_data.py

reset_db:
		@echo 'Este comando vacía la DB e instala fixtures por default.'
		@while [ -z "$$CONTINUE" ]; do \
    read -r -p "Continuar? [y/N] " CONTINUE; \
		done ; \
		[ $$CONTINUE = "y" ] || [ $$CONTINUE = "Y" ] || (echo "Exiting."; exit 1;)
		@$(DJANGO_EXEC) $(FLUSH)
		@$(PYTHON_EXEC) $(LOADDATA)