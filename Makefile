EXE     = register
LIBS    = reg_form.py reg_request_db.py member.py
SRCS    = $(EXE) $(LIBS)

DSTDIR  = /usr/lib/cgi-bin/
DSTS    = $(addprefix $(DSTDIR), $(SRCS))

all: $(DSTS)

$(DSTS): $(SRCS)
	sudo cp $(SRCS) $(DSTDIR)
	sudo chmod 755 $(DSTDIR)$(EXE)
	sudo chmod 644 $(addprefix $(DSTDIR), $(LIBS))
