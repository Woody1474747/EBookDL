import convert
import convert_par
import convert_par_v2
import convert_par_v3
import convert_par_v4

print("Running non parallel conversion")
convert.convert_to_pdf(337, "out.pdf")
print("Running parallel conversion V1")
convert_par.convert_to_pdf_parallel(337, "out_par1.pdf")
print("Running parallel conversion V2")
convert_par_v2.convert_to_pdf_parallel(337, "out_par2.pdf")
print("Running parallel conversion V3")
convert_par_v3.convert_to_pdf_fast(337, "out_par3.pdf")
print("Running parallel conversion V4")
convert_par_v4.convert_to_pdf(337, "out_parv4.pdf")


