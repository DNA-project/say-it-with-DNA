import Chamaeleo.methods.yyc as yyc #YinYang Code
import Chamaeleo.methods.sc as sc #Simple Code
import Chamaeleo.methods.hc as hc #Goldman Code
import Chamaeleo.methods.fc as fc #Fountain Code
import Chamaeleo.methods.gc as gc #Grass Code
import Chamaeleo.codec_factory as codec_factory
from Chamaeleo.methods.verifies import rs #Reed-Solomon Error Correction
import Chamaeleo.methods.verifies.hm as hm #Hamming Error Correction
import argparse
import time


parser = argparse.ArgumentParser()

#basics
parser.add_argument("--show_log", help="do you want to see the progress?; on")
parser.add_argument("--mode", help="choose between encode or decode mode")
parser.add_argument("--input_path", help="path to your input file")
parser.add_argument("--output_path", help="path to your output file")
parser.add_argument("--algorithm", help="choose your algorithm: YinYang, SimpleCode, GoldmanCode, FountainCode, GrassCode") #auswahl der algorithmen vervolllständigen
parser.add_argument("--time", help="prints the runtime")

#Simple Code
parser.add_argument("--mapping_rule", nargs='+',type=int, help="default 0 1 2 3, can be changed to 0 0 1 1)")

#Goldmans Code
parser.add_argument("--fixed_huff", help="if set -> fixed_Huffman = True")

#Grass Code
parser.add_argument("--base_values", help="Grass Code base_values: 48")

#Fountain Code
parser.add_argument("--homopolymer", help="default is 4")
parser.add_argument("--gc_content", help="default is 0.2")
parser.add_argument("--redundancy", help="default is 0.5")
parser.add_argument("--c_dist", help="default is 0.1")
parser.add_argument("--delta", help="default is 0.5")
parser.add_argument("--recursion_depth", help="default is 10000000")
parser.add_argument("--header_size", help="default is 4 (32 bits)")
parser.add_argument("--segment_length", help="default is 120")

#Yin-Yang Code
parser.add_argument("--base_reference", nargs='+',type=int, help="default is Rule 495 [0,1,0,1]by typing 0 1 0 1")
parser.add_argument("--current_code_matrix", nargs='+',type=int, help="default is Rule 495 [[1,1,0,0],[1,0,0,1],[1,1,0,0],[1,1,0,0]];write wit an 1 infront: 1 0 1 0 1 1 0 1 0 1 0 1 0 1 0 1 0")
parser.add_argument("--support_bases", help="default is 4")
parser.add_argument("--support_spacing", help="Spacing between support base and surrent base is 0 (default)")
parser.add_argument("--max_ratio", help="default is 0.8")
parser.add_argument("--search_count", help="default is 1")

#ERROR validation/correction
parser.add_argument("--verify_rs", help="Reed Solomon verification; on")
parser.add_argument("--verify_hm", help="Hamming verification; on")

args = parser.parse_args()


show_log = False

if args.show_log == "on":
    show_log = True
else:
    print("log is off/is not showing as default. Add '--show_log on' as argument if you would like to see it")



if args.mode == "encode":
    print("Welcome in ENcode mode")

    if args.algorithm == "YinYang":

        start1 = time.time()

        #default values
        baseReference = [0,1,0,1]
        currentCodeMatrix = [[1,1,0,0],[1,0,0,1],[1,1,0,0],[1,1,0,0]]
        supportBases = 'A'
        supportSpacing = 0
        maxRatio =0.8
        searchCount = 1

        if args.base_reference:
            baseReference = args.base_reference
            print("You set the base_reference parameter to", args.base_reference)
        if args.current_code_matrix:
            a = args.current_code_matrix # a = [1, 1001, 1010, 1010, 1010]
            currentCodeMatrix = [[a[1],a[2],a[3],a[4]],[a[5],a[6],a[7],a[8]],[a[9],a[10],a[11],a[12]],[a[13],a[14],a[15],a[16]]] # = [[1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 1, 0], [1, 0, 1, 0]]
            print("You set the current_code_matrix parameter to", currentCodeMatrix)
        if args.support_bases:
            supportBases = args.support_bases
            print("You set the support_bases parameter to", args.support_bases)
        if args.support_spacing:
            supportSpacing = int(args.support_spacing)
            print("You set the support_spacing parameter to", args.support_spacing)
        if args.max_ratio:
            maxRatio = float(args.max_ratio)
            print("You set the max_ratio parameter to", args.max_ratio)
        if args.search_count:
            searchCount = int(args.search_count)
            print("You set the search_count parameter to", args.search_count)

        method_yyc = yyc.YYC(base_reference=baseReference,current_code_matrix=currentCodeMatrix, support_bases=supportBases, support_spacing=supportSpacing, max_ratio=maxRatio,search_count=searchCount)

        if args.verify_rs == "on":
            print("Reed-Solomon Verification on")
            verify_rs = rs.RS()
            codec_factory.encode(method=method_yyc, input_path=args.input_path, output_path=args.output_path, model_path="C:\\yyc+rs.pkl", need_log=show_log,need_index=True, verify=verify_rs)

            if args.time == "on":
                end3 = time.time()
                print("encoding Yin-Yang with Reed-Solomon Verification took: ", end3 - start1)

        elif args.verify_hm == "on":
            print("Hamming Verification on")
            verify_hm = hm.Hm()
            codec_factory.encode(method=method_yyc, input_path=args.input_path, output_path=args.output_path, model_path="C:\\yyc+hm.pkl", need_log=show_log, need_index=True, verify=verify_hm)

            if args.time == "on":
                end2 = time.time()
                print("encoding Yin-Yang with Hamming Verification took: ", end2 - start1)

        else:
            codec_factory.encode(method=method_yyc, input_path=args.input_path, output_path=args.output_path, model_path="C:\\yyc.pkl", need_log=show_log)

            if args.time == "on":
                end1 = time.time()
                print("encoding Yin-Yang took: ", end1 - start1)


    if args.algorithm == "SimpleCode":

        start_sc_en = time.time()

        if args.mapping_rule:
            method_sc = sc.SC(mapping_rule=args.mapping_rule)
            print("new mapping rule is applied: ", args.mapping_rule)
        else:
            method_sc = sc.SC()

        if args.verify_rs == "on":
            print("Reed-Solomon Verification on")
            verify_rs = rs.RS()
            codec_factory.encode(method=method_sc, input_path=args.input_path, output_path=args.output_path, model_path="C:\\sc+rs.pkl", need_log=show_log,need_index=True, verify=verify_rs)

            if args.time == "on":
                end_sc_en_rs = time.time()
                print("encoding Simple Code with Reed-Solomon Verification took: ", end_sc_en_rs - start_sc_en)

        elif args.verify_hm == "on":
            print("Hamming Verification on")
            verify_hm = hm.Hm()
            codec_factory.encode(method=method_sc, input_path=args.input_path, output_path=args.output_path, model_path="C:\\sc+hm.pkl", need_log=show_log, need_index=True, verify=verify_hm)

            if args.time == "on":
                end_sc_en_hm = time.time()
                print("encoding Simple Code with Hamming Verification took: ", end_sc_en_hm - start_sc_en)

        else:
            codec_factory.encode(method=method_sc, input_path=args.input_path, output_path=args.output_path, model_path="C:\\sc.pkl", need_log=show_log)

            if args.time == "on":
                end_sc_en = time.time()
                print("encoding Simple Code took: ", end_sc_en - start_sc_en)


    if args.algorithm == "GoldmanCode":

        start_huff_en = time.time()

        if args.fixed_huff == "True":
            print("fixing Huffman tree...")
            method_hc = hc.HC(fixed_huffman=True)
        else:
            method_hc = hc.HC()

        if args.verify_rs == "on":
            print("Reed-Solomon Verification on")
            verify_rs = rs.RS()
            codec_factory.encode(method=method_hc, input_path=args.input_path, output_path=args.output_path, model_path="C:\\hc+rs.pkl", need_log=show_log,need_index=True, verify=verify_rs)

            if args.time == "on":
                end_huff_en_rs = time.time()
                print("encoding Goldman Code with Reed-Solomon Verification took: ", end_huff_en_rs - start_huff_en)

        elif args.verify_hm == "on":
            print("Hamming Verification on")
            verify_hm = hm.Hm()
            codec_factory.encode(method=method_hc, input_path=args.input_path, output_path=args.output_path, model_path="C:\\hc+hm.pkl", need_log=show_log, need_index=True, verify=verify_hm)

            if args.time == "on":
                end_huff_en_hm = time.time()
                print("encoding Goldman Code with Hamming Verification took: ", end_huff_en_hm - start_huff_en)

        else:
            codec_factory.encode(method=method_hc, input_path=args.input_path, output_path=args.output_path, model_path="C:\\hc.pkl", need_log=show_log,need_index=False)

            if args.time == "on":
                end_huff_en = time.time()
                print("encoding Goldman Code took: ", end_huff_en - start_huff_en)


    if args.algorithm == "FountainCode":

        start_Fount_en = time.time()

        print("You're using ",args.algorithm)
        #default values
        homopol = 4
        gc_cont = 0.2
        redun = 0.5
        cDist = 0.1
        f_delta = 0.5
        recursionDepth = 10000000
        headerSize = 4
        # decode_packets = None
        segmentLength = 120

        if args.homopolymer:
            homopol = int(args.homopolymer)
            print("You set the homopolymer parameter to", args.homopolymer)
        if args.gc_content:
            gc_cont = float(args.gc_content)
            print("You set the gc_content parameter to", args.gc_content)
        if args.redundancy:
            redun = float(args.redundancy)
            print("You set the redundancy parameter to", args.redundancy)
        if args.c_dist:
            cDist = float(args.c_dist)
            print("You set the c_dist parameter to", args.c_dist)
        if args.delta:
            f_delta = float(args.delta)
            print("You set the delta parameter to", args.delta)
        if args.recursion_depth:
            recursionDepth = int(args.recursion_depth)
            print("You set the recursion_depth parameter to", args.recursion_depth)
        if args.header_size:
            headerSize = int(args.header_size)
            print("You set the header_size parameter to", args.header_size)
        if args.segment_length:
            segmentLength = int(args.segment_length)
            print("You set the segment_length parameter to", args.segment_length)

        method_fc = fc.FC(homopolymer= homopol, gc_content=gc_cont,redundancy=redun,c_dist=cDist, delta=f_delta, recursion_depth=recursionDepth, header_size=headerSize)

        if args.verify_rs == "on":
            print("Reed-Solomon Verification on")
            verify_rs = rs.RS()
            codec_factory.encode(method=method_fc, input_path=args.input_path, output_path=args.output_path, need_log=show_log, model_path="C:\\fc+rs.pkl", segment_length=segmentLength, need_index=True,verify=verify_rs)

            if args.time == "on":
                end_Fount_en_rs = time.time()
                print("encoding Fountain Code with Reed-Solomon Verification took: ", end_Fount_en_rs - start_Fount_en)

        elif args.verify_hm == "on":
            print("Hamming Verification on")
            verify_hm = hm.Hm()
            #funktioniert mit segment length = 119
            codec_factory.encode(method=method_fc, input_path=args.input_path, output_path=args.output_path, model_path="C:\\fc+hm.pkl", need_log=show_log, need_index=True, verify=verify_hm, segment_length = segmentLength)

            if args.time == "on":
                end_Fount_en_hm = time.time()
                print("encoding Fountain Code with Hamming Verification took: ", end_Fount_en_hm - start_Fount_en)

        else:
            codec_factory.encode(method=method_fc, input_path=args.input_path, output_path=args.output_path, need_log=show_log,need_index=False, model_path="C:\\fc.pkl", segment_length = segmentLength)#segment_length = 119

            if args.time == "on":
                end_Fount_en = time.time()
                print("encoding Fountain Code took: ", end_Fount_en - start_Fount_en)


    if args.algorithm == "GrassCode":

        start_Reed_en = time.time()
        print("You're using ",args.algorithm)

        if args.base_values:
            method_gc = gc.GC([index for index in range(int(args.base_values))])
        else:
            method_gc = gc.GC()

        if args.verify_rs == "on":
            print("Reed-Solomon Verification on")
            verify_rs = rs.RS()
            codec_factory.encode(method=method_gc, input_path=args.input_path, output_path=args.output_path, model_path="C:\\gc+rs.pkl", need_log=show_log, need_index=True, verify=verify_rs)

            if args.time == "on":
                end_Reed_en_rs = time.time()
                print("encoding Grass Code with Reed-Solomon Verification took: ", end_Reed_en_rs - start_Reed_en)

        elif args.verify_hm == "on":
            print("Hamming Verification on")
            verify_hm = hm.Hm()
            codec_factory.encode(method=method_gc, input_path=args.input_path, output_path=args.output_path,model_path="C:\\gc+hm.pkl", need_log=show_log, need_index=True, verify=verify_hm)

            if args.time == "on":
                end_Reed_en_hm = time.time()
                print("encoding Grass Code with Hamming Verification took: ", end_Reed_en_hm - start_Reed_en)

        else:
            codec_factory.encode(method_gc, input_path=args.input_path, output_path=args.output_path, need_log=show_log, model_path="C:\\gc.pkl", need_index=True)

            if args.time == "on":
                end_Reed_en = time.time()
                print("encoding Grass Code took: ", end_Reed_en - start_Reed_en)

    print("encoded", args.input_path, "successfully with", args.algorithm, "Algorithm")


if args.mode == "decode":
    print("Welcome in DEcode mode")
    start_yyc_de = time.time()

    if args.algorithm == "YinYang":
        if args.verify_rs == "on":
            print("Reed-Solomon Verification on")
            codec_factory.decode(model_path="C:\\yyc+rs.pkl", input_path=args.input_path, output_path=args.output_path,need_log=show_log, has_index=True)

            if args.time == "on":
                end_yyc_de_rs = time.time()
                print("decoding Yin-Yang with Reed-Solomon Verification took: ", end_yyc_de_rs - start_yyc_de)

        elif args.verify_hm == "on":
            print("Hamming Verification on")
            codec_factory.decode(model_path="C:\\yyc+hm.pkl", input_path=args.input_path, output_path=args.output_path, need_log=show_log, has_index=True)

            if args.time == "on":
                end_yyc_de_hm = time.time()
                print("decoding Yin-Yang with Hamming Verification took: ", end_yyc_de_hm - start_yyc_de)

        else:
            codec_factory.decode(model_path="C:\\yyc.pkl", input_path=args.input_path, output_path=args.output_path, need_log=show_log)

            if args.time == "on":
                end_yyc_de = time.time()
                print("decoding Yin-Yang took: ", end_yyc_de - start_yyc_de)

    if args.algorithm == "SimpleCode":

        start_sc_de = time.time()

        if args.verify_rs == "on":
            print("Reed-Solomon Verification on")
            codec_factory.decode(model_path="C:\\sc+rs.pkl", input_path=args.input_path, output_path=args.output_path,need_log=show_log, has_index=True)

            if args.time == "on":
                end_sc_de_rs = time.time()
                print("decoding Simple Code with Reed-Solomon Verification took: ", end_sc_de_rs - start_sc_de)

        elif args.verify_hm == "on":
            print("Hamming Verification on")
            codec_factory.decode(model_path="C:\\sc+hm.pkl", input_path=args.input_path, output_path=args.output_path, need_log=show_log, has_index=True)

            if args.time == "on":
                end_sc_de_hm = time.time()
                print("decoding Simple Code with Hamming Verification took: ", end_sc_de_hm - start_sc_de)

        else:
            codec_factory.decode(model_path="C:\\sc.pkl", input_path=args.input_path, output_path=args.output_path, need_log=show_log)

            if args.time == "on":
                end_sc_de = time.time()
                print("decoding Simple Code took: ", end_sc_de - start_sc_de)


    if args.algorithm == "GoldmanCode":

        start_huff_de = time.time()

        if args.verify_rs == "on":
            print("Reed-Solomon Verification on")
            codec_factory.decode(model_path="C:\\hc+rs.pkl", input_path=args.input_path, output_path=args.output_path, need_log=show_log, has_index=True)

            if args.time == "on":
                end_huff_de_rs = time.time()
                print("decoding Goldman Code with Reed-Solomon Verification took: ", end_huff_de_rs - start_huff_de)

        elif args.verify_hm == "on":
            print("Hamming Verification on")
            codec_factory.decode(model_path="C:\\hc+hm.pkl", input_path=args.input_path, output_path=args.output_path, need_log=show_log, has_index=True)

            if args.time == "on":
                end_huff_de_hm = time.time()
                print("decoding Goldman Code with Hamming Verification took: ", end_huff_de_hm - start_huff_de)

        else:
            codec_factory.decode(model_path="C:\\hc.pkl", input_path=args.input_path, output_path=args.output_path, has_index=False, need_log=show_log)

            if args.time == "on":
                end_huff_de = time.time()
                print("decoding Goldman Code took: ", end_huff_de - start_huff_de)



    if args.algorithm == "FountainCode":

        start_Fount_de = time.time()

        if args.verify_rs == "on":
            print("Reed-Solomon Verification on")
            codec_factory.decode(model_path="C:\\fc+rs.pkl", input_path=args.input_path, output_path=args.output_path, need_log=show_log, has_index=True)

            if args.time == "on":
                end_Fount_de_rs = time.time()
                print("decoding Fountain Code with Reed-Solomon Verification took: ", end_Fount_de_rs - start_Fount_de)

        elif args.verify_hm == "on":
            print("Hamming Verification on")
            codec_factory.decode(model_path="C:\\fc+hm.pkl", input_path=args.input_path, output_path=args.output_path, need_log=show_log, has_index=True)

            if args.time == "on":
                end_Fount_de_hm = time.time()
                print("decoding Fountain Code with Hamming Verification took: ", end_Fount_de_hm - start_Fount_de)
        else:
            codec_factory.decode(model_path="C:\\fc.pkl", input_path=args.input_path, output_path=args.output_path, need_log=show_log, has_index=False)

            if args.time == "on":
                end_Fount_de = time.time()
                print("decoding Fountain Code took: ", end_Fount_de - start_Fount_de)


    if args.algorithm == "GrassCode":

        start_Reed_de = time.time()

        if args.verify_rs == "on":
            print("Reed-Solomon Verification on")
            codec_factory.decode(model_path="C:\\gc+rs.pkl", input_path=args.input_path, output_path=args.output_path, need_log=show_log, has_index=True)

            if args.time == "on":
                end_Reed_de_rs = time.time()
                print("decoding Grass Code with Reed-Solomon Verification took: ", end_Reed_de_rs - start_Reed_de)

        elif args.verify_hm == "on":
            print("Hamming Verification on")
            codec_factory.decode(model_path="C:\\gc+hm.pkl", input_path=args.input_path, output_path=args.output_path, need_log=show_log, has_index=True)

            if args.time == "on":
                end_Reed_de_hm = time.time()
                print("decoding Grass Code with Hamming Verification took: ", end_Reed_de_hm - start_Reed_de)

        else:
            codec_factory.decode(model_path="C:\\gc.pkl", input_path=args.input_path, output_path=args.output_path, need_log=show_log, has_index=True)

            if args.time == "on":
                end_Reed_de = time.time()
                print("decoding Grass Code took: ", end_Reed_de - start_Reed_de)

    print("decoded", args.input_path,"successfully with", args.algorithm,"Algorithm")
