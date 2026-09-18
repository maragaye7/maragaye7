import { useEffect,useState } from "react";
import { View,Text,TextInput,FlatList,StyleSheet } from "react-native";
import { apiGet } from "../services/api";

export default function Clients(){
 const [rows,setRows]=useState<any[]>([]); const [q,setQ]=useState("");
 async function load(){setRows(await apiGet(`/clients${q?`?q=${encodeURIComponent(q)}`:""}`));}
 useEffect(()=>{load()},[]);
 return <View style={s.page}><TextInput style={s.search} placeholder="Rechercher un client" value={q} onChangeText={setQ} onSubmitEditing={load}/>
 <FlatList data={rows} keyExtractor={(x)=>String(x.id)} renderItem={({item})=><View style={s.row}><Text style={s.name}>{item.name ?? item.nom ?? item.ref}</Text><Text style={s.meta}>{item.email ?? item.town ?? "Client Dolibarr"}</Text></View>}/></View>
}
const s=StyleSheet.create({page:{flex:1,padding:16,backgroundColor:"#F7F9F8"},search:{backgroundColor:"#fff",padding:14,borderRadius:12,marginBottom:12},row:{backgroundColor:"#fff",padding:16,borderRadius:12,marginBottom:8},name:{fontWeight:"700",fontSize:16},meta:{color:"#667085",marginTop:4}});
