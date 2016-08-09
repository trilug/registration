HOST = $(shell hostname)
ifeq ($(HOST), pilot)
	STEERING_DIR = /usr/lib/steering-cgi/
else
	STEERING_DIR = /usr/lib/cgi-bin/
endif
MAIN_DIR = /usr/lib/cgi-bin/

STEERING_EXES = process_registrations
STEERING_LIBS = process_form.py
STEERING_SRCS = $(STEERING_EXES) $(STEERING_LIBS)
STEERING_DSTS = $(addprefix $(STEERING_DIR), $(STEERING_SRCS))

MAIN_EXES = request_membership
MAIN_LIBS = register.py reg_form.py reg_request_db.py reg_scrub.py member.py
MAIN_SRCS = $(MAIN_EXES) $(MAIN_LIBS)
MAIN_DSTS = $(addprefix $(MAIN_DIR), $(MAIN_SRCS))

SRCS = $(STEERING_SRCS) $(MAIN_SRCS)
DSTS = $(STEERING_DSTS) $(MAIN_DSTS)

all: $(DSTS)

$(DSTS): $(SRCS)
	sudo cp $(MAIN_SRCS) $(MAIN_DIR)
	sudo chmod 755 $(addprefix $(MAIN_DIR), $(MAIN_EXES))
	sudo chmod 644 $(addprefix $(MAIN_DIR), $(MAIN_LIBS))
	sudo cp $(STEERING_SRCS) $(STEERING_DIR)
	sudo chmod 755 $(addprefix $(STEERING_DIR), $(STEERING_EXES))
	sudo chmod 644 $(addprefix $(STEERING_DIR), $(STEERING_LIBS))
ifneq ($(STEERING_DIR), $(MAIN_DIR))
	sudo ln -s -f $(addprefix $(MAIN_DIR), $(MAIN_LIBS)) $(STEERING_DIR)
endif
