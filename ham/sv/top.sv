// --------------------------------------------------------------
// Copyright 2021
// --------------------------------------------------------------

module top();

   logic clk;
   logic reset_n;
   logic [3:0] inp_data;
   logic [3:0] gen_code;
   logic       is_error;
   logic       is_fatal;
   logic [3:0] out_data;

/* verilator lint_off STMTDLY */
   always #15 clk = ~clk;

   initial begin
      clk = 1'b0;
      reset_n = 1'b1;
      #50 reset_n = 1'b0;
   end
/* verilator lint_on STMTDLY */

   // Instantiate the generate module
   ham_generate_8_4 u_gen_8_4
     ( .data_i (inp_data),
       .code_o (gen_code));

   // Instantiate the check module
   ham_check_8_4 u_chk_8_4
     ( .data_i           (inp_data),
       .code_i           (gen_code),
       .error_o          (is_error),
       .fatal_o          (is_fatal),
       .corrected_data_o (out_data));

endmodule // top
