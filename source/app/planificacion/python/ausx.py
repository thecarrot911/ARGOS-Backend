for num_semana in range(len(cont_semana)):
        work_extra = list_turno_extra[num_semana]
        if(work_extra>=1):
            for i in range(list_turno_extra[num_semana]):
                if(mes[num_semana][i][0]==meses_anio[month-1]):
                    list_index_itinerario = ItinerarioFunction(mes[num_semana][i][1], itinerario)
                    if((i<=5) and (work_extra>=1)): # ASIGNACIÓN EN LA MAÑANA
                        print(mes[num_semana][i][1])
                        if(len(list_index_itinerario)==0):
                            model.Add(list_itinerario[num_semana][i][0]==2)
                            work_extra = work_extra - 1
                            cant_turnos_totales[0] = cant_turnos_totales[0] + 1

                        elif((len(list_index_itinerario)==1) and (itinerario[list_index_itinerario[0]][1]!=1) and (itinerario[list_index_itinerario[0]][2]+cant_turno-1<num_empleado)):
                            model.Add(list_itinerario[num_semana][i][0]==2)
                            work_extra = work_extra - 1
                            cant_turnos_totales[0] = cant_turnos_totales[0] + 1

                        elif((len(list_index_itinerario)==1 or len(list_index_itinerario)>=2) and (i<5)):
                            model.Add(list_itinerario[num_semana][i+1][0]==2)
                            work_extra = work_extra -1
                            cant_turnos_totales[0] = cant_turnos_totales[0] + 1

                        elif((len(list_index_itinerario)==1 or len(list_index_itinerario)>=2) and (itinerario[list_index_itinerario[0]][1]!=1) and i==5):
                            model.Add(list_itinerario[num_semana+1][0][1]==2)
                            work_extra = work_extra - 1
                            cant_turnos_totales[0] = cant_turnos_totales[0] + 1
                        else: 
                            print(mes[num_semana][i][1])
                            print("else1")

                    elif((i==6) and (work_extra>=1)): # ASIGNACIÓN EN LA TARDE
                        for i in range(5):
                            if(len(list_index_itinerario)==0 and (work_extra>=1)):
                                model.Add(list_itinerario[num_semana][i][1]==2)
                                work_extra = work_extra - 1
                                cant_turnos_totales[1] = cant_turnos_totales[1] + 1

                            elif((len(list_index_itinerario)==1) and (itinerario[list_index_itinerario[0]][1]!=2) and (itinerario[list_index_itinerario[0]][2]+cant_turno-1<num_empleado) and (work_extra>=1)):
                                model.Add(list_itinerario[num_semana][i][1]==2)
                                work_extra = work_extra - 1
                                cant_turnos_totales[1] = cant_turnos_totales[1] + 1

                            elif((len(list_index_itinerario)==1 or len(list_index_itinerario)>=2) and (i<5) and (work_extra>=1)):
                                model.Add(list_itinerario[num_semana][i+1][1]==2)

                                work_extra = work_extra -1
                                cant_turnos_totales[1] = cant_turnos_totales[1] + 1



                else: 
                    if((i<=5) and (work_extra>=1)): # ASIGNACIÓN EN LA MAÑANA
                        if(len(list_index_itinerario)==0):
                            model.Add(list_itinerario[num_semana][i][0]==2)

                            work_extra = work_extra - 1
                            cant_turnos_totales[0] = cant_turnos_totales[0] + 1

                    elif((i==6) and (work_extra>=1)): # ASIGNACIÓN EN LA TARDE
                        for i in range(5):
                            if(len(list_index_itinerario)==0 and (work_extra>=1)):
                                model.Add(list_itinerario[num_semana][i][1]==2)
                                work_extra = work_extra - 1
                                cant_turnos_totales[1] = cant_turnos_totales[1] + 1