help:
	@echo
	@echo "Targets:"
	@echo "--------"
	@echo "  1. compile"
	@echo "  2. clean"

compile:
	@verilator -sv -Wall top.sv --lint-only
clean:
	rm -r obj_dir
