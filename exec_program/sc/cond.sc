
import io.shiftleft.codepropertygraph.generated.nodes.{Member, Method}
import io.shiftleft.dataflowengineoss.language._
import io.shiftleft.semanticcpg.language._



@main def main(cpgFile:String, outFile:String):Unit = {
	importCpg(cpgFile)
	
	cpg.controlStructure.map(x=>List(
       x.file.name.l,
       x.lineNumber,
       x.method.name,
       x.controlStructureType,
       x.condition.isCall.argument.code.l,
       x.astMinusRoot.isCall.lineNumber.l,
       x.code )
       ).toJson |> outFile 

	
}
