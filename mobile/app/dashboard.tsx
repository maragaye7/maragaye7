import { useEffect,useState } from "react";
import { View,Text,Pressable,StyleSheet,ScrollView } from "react-native";
import { router } from "expo-router";
import { apiGet } from "../services/api";

export default function Dashboard(){
 const [data,setData]=useState<any>(null);
 useEffect(()=>{apiGet("/dashboard").then(setData).catch(()=>router.replace("/login"));},[]);
 return <ScrollView contentContainerStyle={s.page}>
  <Text style={s.hello}>MGA Mobile</Text><Text style={s.title}>Tableau de bord</Text>
  <View style={s.grid}>{(data?.kpis??[]).map((k:any)=><View style={s.card} key={k.label}><Text style={s.value}>{k.value}</Text><Text>{k.label}</Text></View>)}</View>
  <Text style={s.section}>Actions rapides</Text>
  <Pressable style={s.action} onPress={()=>router.push("/clients")}><Text>👥 Clients</Text></Pressable>
  <Pressable style={s.action} onPress={()=>router.push("/products")}><Text>📦 Catalogue produits</Text></Pressable>
  <View style={s.disabled}><Text>📄 Nouveau devis — Sprint 2</Text></View>
  <View style={s.disabled}><Text>✨ Assistant MGA IA — à venir</Text></View>
 </ScrollView>
}
const s=StyleSheet.create({
 page:{padding:20,paddingTop:70,backgroundColor:"#F7F9F8",flexGrow:1},
 hello:{color:"#08783e",fontWeight:"800",fontSize:18},title:{fontSize:28,fontWeight:"800",marginBottom:18},
 grid:{flexDirection:"row",flexWrap:"wrap",gap:10},card:{width:"48%",backgroundColor:"#fff",padding:18,borderRadius:14},
 value:{fontSize:20,fontWeight:"800",color:"#08783e"},section:{fontSize:18,fontWeight:"700",marginTop:24,marginBottom:10},
 action:{backgroundColor:"#fff",padding:18,borderRadius:12,marginBottom:10},disabled:{backgroundColor:"#EAECF0",padding:18,borderRadius:12,marginBottom:10}
});
