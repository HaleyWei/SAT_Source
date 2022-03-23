
import io.shiftleft.codepropertygraph.generated.nodes.{Member, Method}
import io.shiftleft.dataflowengineoss.language._
import io.shiftleft.semanticcpg.language._




@main def main(cpgFile:String, outFile:String):Unit = {
	importCpg(cpgFile)
	cpg.ret.map(x=>(
       x.lineNumber,
       x.file.name.l,
       x.method.name,
       x.astChildren.isExpression.map(argu=>(argu.code,argu.typ.typeDeclFullName.l)).l,
       x.code)).toJson |> outFile
	
}
