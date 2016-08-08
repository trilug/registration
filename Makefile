EXES    = request_membership process_registrations
LIBS    = register.py reg_form.py reg_request_db.py reg_scrub.py member.py process_form.py
SRCS    = $(EXES) $(LIBS)

DSTDIR  = /usr/lib/cgi-bin/
DSTS    = $(addprefix $(DSTDIR), $(SRCS))

all: $(DSTS)

$(DSTS): $(SRCS)
	sudo cp $(SRCS) $(DSTDIR)
	sudo chmod 755 $(addprefix $(DSTDIR), $(EXES))
	sudo chmod 644 $(addprefix $(DSTDIR), $(LIBS))
