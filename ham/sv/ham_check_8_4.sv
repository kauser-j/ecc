// --------------------------------------------------------------
// Copyright 2021
// --------------------------------------------------------------

module ham_check_8_4
  (
   input  wire [3:0]  data_i,
   input  wire [3:0]  code_i,
   output wire 	      error_o,
   output wire 	      fatal_o,
   output wire [3:0]  corrected_data_o
  );

   // ECC Key:
   // -------
   // [7] [6] [5] [4] [3] [2] [1] [0]
   //  1   0   0   0   1   1   0   1  -> syndrome bit [3]
   //  0   1   0   0   0   1   1   1  -> syndrome bit [2]
   //  0   0   1   0   1   1   1   0  -> syndrome bit [1]
   //  0   0   0   1   1   0   1   1  -> syndrome bit [0]

   // Signal declarations
   logic [3:0] 	      syndrome;
   logic 	      syndrome_0;
   logic [7:0] 	      syndrome_c;

   // Generate syndrome
   assign syndrome[3] = code_i[3] ^ (data_i[3] ^ data_i[2] ^ data_i[0]);
   assign syndrome[2] = code_i[2] ^ (^(data_i[2:0]));
   assign syndrome[1] = code_i[1] ^ (^(data_i[2:1]));
   assign syndrome[0] = code_i[0] ^ (data_i[3] ^ (^(data_i[1:0])));

   // Decode syndrome
   assign syndrome_0    = syndrome=='h0;
   assign syndrome_c[7] = syndrome==4'b1000; // Error in code
   assign syndrome_c[6] = syndrome==4'b0100; // Error in code
   assign syndrome_c[5] = syndrome==4'b0010; // Error in code
   assign syndrome_c[4] = syndrome==4'b0001; // Error in code
   assign syndrome_c[3] = syndrome==4'b1011; // Error in bit3
   assign syndrome_c[2] = syndrome==4'b1110; // Error in bit2
   assign syndrome_c[1] = syndrome==4'b0111; // Error in bit1
   assign syndrome_c[0] = syndrome==4'b1101; // Error in bit0

   // There is an error if the syndrome isn't 0. This is the simplest
   // level of decode
   assign error_o = ~syndrome_0;

   // The error is fatal if the syndrome is non-0 and doesn't
   // match any of the correctable syndromes
   assign fatal_o = ~syndrome_0 & (~|syndrome_c);

   // The corrected data is decoded syndrome xor with the original
   // data. Typically on no error syndrome is 0, therefore an exclusive
   // or will preserve the original data which is what we want.
   assign corrected_data_o = data_i ^ syndrome_c[3:0];

endmodule // ham_check_8_4
