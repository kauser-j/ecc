// --------------------------------------------------------------
// Copyright 2021
// --------------------------------------------------------------

module ham_generate_8_4
  (
   input  wire [3:0] data_i,
   output wire [3:0] code_o
  );

   // ECC Key:
   // -------
   // [3] [2] [1] [0]
   //  1   1   0   1  -> parity check bit [3]
   //  0   1   1   1  -> parity check bit [2]
   //  1   1   1   0  -> parity check bit [1]
   //  1   0   1   1  -> parity check bit [0]

   assign code_o[3] = (data_i[3] ^ data_i[2] ^ data_i[0]);
   assign code_o[2] = (^(data_i[2:0]));
   assign code_o[1] = (^(data_i[3:1]));
   assign code_o[0] = (data_i[3] ^ (^(data_i[1:0])));

endmodule // ham_generate_8_4
