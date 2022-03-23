
import io.shiftleft.codepropertygraph.generated.nodes.{Member, Method}
import io.shiftleft.dataflowengineoss.language._
import io.shiftleft.semanticcpg.language._



@main def main(cpgFile:String, outFile:String):Unit = {
	importCpg(cpgFile)
	cpg.call.filterNot(_.name.contains("<operator>")).map(call_node=>( 
       call_node.name, 
       call_node.file.name.l, 
       call_node.method.name, 
       call_node.argument.map(argu=>(argu.code,argu.typ.typeDeclFullName.l)).l, 
       call_node.lineNumber, 
       call_node.code)).toJson |> outFile
	
}
