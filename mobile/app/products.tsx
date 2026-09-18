import { useEffect,useState } from "react";
import { View,Text,TextInput,FlatList,StyleSheet } from "react-native";
import { apiGet } from "../services/api";

export default function Products(){
 const [rows,setRows]=useState<any[]>([]); const [q,setQ]=useState("");
 async function load(){setRows(await apiGet(`/products${q?`?q=${encodeURIComponent(q)}`:""}`));}
 useEffect(()=>{load()},[]);
 return <View style={s.page}><TextInput style={s.search} placeholder="Référence produit" value={q} onChangeText={setQ} onSubmitEditing={load}/>
 <FlatList data={rows} keyExtractor={(x)=>String(x.id)} renderItem={({item})=><View style={s.row}><Text style={s.ref}>{item.ref}</Text><Text style={s.name}>{item.label ?? "Produit"}</Text><Text style={s.price}>{item.price ? `${Number(item.price).toLocaleString("fr-FR")} FCFA HT` : "Prix non disponible"}</Text></View>}/></View>
}
const s=StyleSheet.create({page:{flex:1,padding:16,backgroundColor:"#F7F9F8"},search:{backgroundColor:"#fff",padding:14,borderRadius:12,marginBottom:12},row:{backgroundColor:"#fff",padding:16,borderRadius:12,marginBottom:8},ref:{color:"#08783e",fontWeight:"800"},name:{fontWeight:"600",marginTop:4},price:{marginTop:7,color:"#475467"}});
