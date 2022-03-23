
import io.shiftleft.codepropertygraph.generated.nodes.{Member, Method}
import io.shiftleft.dataflowengineoss.language._
import io.shiftleft.semanticcpg.language._

@main def main(cpgFile:String, outFile:String):Unit = {
	importCpg(cpgFile)
	var malloc_data = cpg.call("malloc").map(x=>(x.lineNumber,x.method.filename,x.method.name,"malloc",x.argument(1).code)).l 
	var realloc_data = cpg.call("realloc").map(x=>(x.lineNumber,x.method.filename,x.method.name,"realloc",x.argument(1).code,x.argument(2).code)).l
	var calloc_data = cpg.call("calloc").map(x=>(x.lineNumber,x.method.filename,x.method.name,"calloc",x.argument(1).code,x.argument(2).code)).l
	var alloc_data = cpg.call("ALLOCA").map(x=>(x.lineNumber,x.method.filename,x.method.name,"ALLOCA",x.argument(1).code)).l
	var result = malloc_data ::: realloc_data ::: calloc_data ::: alloc_data
	result |> outFile
	
}
