def init_db():
    """Initialize database data"""
    try:
        from models import ModelDescription, ProjectGoal, FPYAutoData
        from extensions import db
        
        print("Initializing database data...")
        
        # Check model data
        model_count = ModelDescription.query.count()
        print(f"Current model count: {model_count}")
        
        if model_count == 0:
            print("Importing model data...")
            models_data = [
                {"model_name": "A666L_F069", "technology": "4G", "position": "MID", "brand": "Itel", "goal": "93%"},
                {"model_name": "P663LN_F069", "technology": "4G", "position": "MID", "brand": "Itel", "goal": "93%"},
                {"model_name": "X6526_V658A", "technology": "4G", "position": "MID", "brand": "Infinix", "goal": "93%"},
                {"model_name": "BG7_XE674S", "technology": "4G", "position": "MID", "brand": "Tecno", "goal": "93%"},
                {"model_name": "it9020_LS2002", "technology": "2G", "position": "FP", "brand": "Itel", "goal": "NA"},
                {"model_name": "P661N_H334", "technology": "5G", "position": "MID", "brand": "Itel", "goal": "93%"},
                {"model_name": "it2165S_G1808", "technology": "2G", "position": "FP", "brand": "Itel", "goal": "NA"},
                {"model_name": "LI9_H335", "technology": "5G", "position": "MID", "brand": "Tecno", "goal": "93%"},
                {"model_name": "X6851_P865A", "technology": "5G", "position": "HIGH", "brand": "Infinix", "goal": "90%"},
                {"model_name": "S667LN_H6933", "technology": "4G", "position": "LOW", "brand": "Itel", "goal": "93%"},
                {"model_name": "it2175P_G1808", "technology": "2G", "position": "FP", "brand": "Itel", "goal": "NA"},
                {"model_name": "CL7k_P765A", "technology": "5G", "position": "HIGH", "brand": "Tecno", "goal": "90%"},
                {"model_name": "X6851B_P865A", "technology": "5G", "position": "HIGH", "brand": "Infinix", "goal": "90%"},
                {"model_name": "X6871_H962", "technology": "5G", "position": "HIGH", "brand": "Infinix", "goal": "90%"},
                {"model_name": "CL7_P765A", "technology": "5G", "position": "HIGH", "brand": "Tecno", "goal": "90%"},
                {"model_name": "CL9_H961", "technology": "5G", "position": "HIGH", "brand": "Tecno", "goal": "90%"},
                {"model_name": "X6852_P775A", "technology": "5G", "position": "HIGH", "brand": "Infinix", "goal": "90%"},
                {"model_name": "KJ8_H338", "technology": "5G", "position": "MID", "brand": "Tecno", "goal": "93%"},
                {"model_name": "A667LP_SQ373", "technology": "4G", "position": "LOW", "brand": "Itel", "goal": "93%"},
                {"model_name": "X6838_P755A", "technology": "5G", "position": "MID", "brand": "Infinix", "goal": "93%"},
                {"model_name": "A669L_SQ375", "technology": "4G", "position": "LOW", "brand": "Itel", "goal": "93%"},
                {"model_name": "Flip1_MA2432", "technology": "2G", "position": "FP", "brand": "Itel", "goal": "NA"},
                {"model_name": "X6861_H963", "technology": "5G", "position": "FLAGSHIP", "brand": "Infinix", "goal": "90%"},
                {"model_name": "KL4_F201", "technology": "4G", "position": "LOW", "brand": "Tecno", "goal": "93%"},
                {"model_name": "AE10_H833", "technology": "5G", "position": "FOLD", "brand": "Tecno", "goal": "90%"},
                {"model_name": "AE11_H911", "technology": "5G", "position": "FOLD", "brand": "Tecno", "goal": "90%"},
                {"model_name": "X6720_H353", "technology": "5G", "position": "MID", "brand": "Infinix", "goal": "93%"},
                {"model_name": "KL8_H353", "technology": "5G", "position": "LOW", "brand": "Tecno", "goal": "93%"},
                {"model_name": "A671LC_SQ378", "technology": "4G", "position": "MID", "brand": "Itel", "goal": "93%"},
                {"model_name": "X6962_H911", "technology": "5G", "position": "FOLD", "brand": "Infinix", "goal": "90%"},
                {"model_name": "KL8h_H353", "technology": "5G", "position": "LOW", "brand": "Tecno", "goal": "93%"},
                {"model_name": "KD68CS_KD68CS", "technology": "2G", "position": "FP", "brand": "Nexgo", "goal": "NA"},
                {"model_name": "KL4H_XE679", "technology": "4G", "position": "LOW", "brand": "Tecno", "goal": "93%"},
                {"model_name": "IT5032_ET2436", "technology": "2G", "position": "FP", "brand": "Itel", "goal": "NA"},
                {"model_name": "P120_M2001", "technology": "2G", "position": "FP", "brand": "Itel", "goal": "NA"},
                {"model_name": "Ace2p_G1808", "technology": "2G", "position": "FP", "brand": "Itel", "goal": "NA"},
                {"model_name": "It5361_MM61117", "technology": "2G", "position": "FP", "brand": "Itel", "goal": "NA"},
                {"model_name": "It2175P_G1808", "technology": "2G", "position": "FP", "brand": "Itel", "goal": "NA"},
                {"model_name": "P450_MM61120", "technology": "2G", "position": "FP", "brand": "Itel", "goal": "NA"},
                {"model_name": "ACE2L-H_GS1819", "technology": "2G", "position": "FP", "brand": "Itel", "goal": "NA"},
                {"model_name": "It5262_WDS076", "technology": "2G", "position": "FP", "brand": "Itel", "goal": "NA"},
                {"model_name": "It-5095_EY2820", "technology": "2G", "position": "FP", "brand": "Itel", "goal": "NA"},
                {"model_name": "X6532C_MF380", "technology": "4G", "position": "MID", "brand": "Infinix", "goal": "93%"},
                {"model_name": "A671N_H353", "technology": "5G", "position": "MID", "brand": "Itel", "goal": "93%"},
                {"model_name": "it3010A_ET1827", "technology": "2G", "position": "FP", "brand": "Itel", "goal": "NA"},
                {"model_name": "BG6m (Export)_F069M", "technology": "4G", "position": "LOW", "brand": "Tecno", "goal": "93%"},
                {"model_name": "KL5 (Export)_XK678", "technology": "4G", "position": "LOW", "brand": "Tecno", "goal": "93%"},
                {"model_name": "X6857B_H782", "technology": "5G", "position": "HIGH", "brand": "Infinix", "goal": "90%"},
                {"model_name": "CL7 (Export)Eithopia_P765A", "technology": "5G", "position": "HIGH", "brand": "Tecno", "goal": "90%"},
                {"model_name": "X6870_H781", "technology": "5G", "position": "HIGH", "brand": "Infinix", "goal": "90%"},
                {"model_name": "A6610L_SQ372", "technology": "4G", "position": "LOW", "brand": "Itel", "goal": "93%"},
                {"model_name": "It-5608N_G1808", "technology": "2G", "position": "FP", "brand": "Itel", "goal": "NA"},
                {"model_name": "It-9310_LS2801", "technology": "2G", "position": "FP", "brand": "Itel", "goal": "NA"},
                {"model_name": "it2181A_ET1828", "technology": "2G", "position": "FP", "brand": "Itel", "goal": "NA"},
                {"model_name": "A6610L(Export) Latin America_SQ372", "technology": "4G", "position": "LOW", "brand": "Itel", "goal": "93%"},
                {"model_name": "LJ8_H781", "technology": "5G", "position": "LOW", "brand": "Tecno", "goal": "93%"},
                {"model_name": "M3501_M819N", "technology": "5G", "position": "MID", "brand": "INDKAL", "goal": "93%"},
                {"model_name": "KL5-V_XK678", "technology": "5G", "position": "LOW", "brand": "Tecno", "goal": "93%"},
                {"model_name": "C671L_SM382", "technology": "4G", "position": "LOW", "brand": "Itel", "goal": "93%"},
                {"model_name": "LJ8K_H781", "technology": "5G", "position": "LOW", "brand": "Tecno", "goal": "93%"},
                {"model_name": "X6525_F069", "technology": "4G", "position": "LOW", "brand": "Infinix", "goal": "93%"},
                {"model_name": "A663L_V450A", "technology": "4G", "position": "LOW", "brand": "Itel", "goal": "93%"},
                {"model_name": "KM4_F151", "technology": "4G", "position": "LOW", "brand": "Tecno", "goal": "93%"},
                {"model_name": "LJ7_H782", "technology": "5G", "position": "MID", "brand": "Tecno", "goal": "93%"},
                {"model_name": "X6726_P526A", "technology": "5G", "position": "MID", "brand": "Infinix", "goal": "93%"},
                {"model_name": "V230_GK2819", "technology": "2G", "position": "FP", "brand": "VILLAON", "goal": "NA"},
                {"model_name": "V220_GY2433", "technology": "2G", "position": "FP", "brand": "VILLAON", "goal": "NA"},
                {"model_name": "IT9120_SL24B", "technology": "4G", "position": "FP", "brand": "Itel", "goal": "NA"},
                {"model_name": "X6725_F151", "technology": "4G", "position": "LOW", "brand": "Infinix", "goal": "93%"},
                {"model_name": "X6876_H786", "technology": "5G", "position": "HIGH", "brand": "Infinix", "goal": "90%"},
                {"model_name": "X6730_H358", "technology": "5G", "position": "MID", "brand": "Infinix", "goal": "93%"},
                {"model_name": "KM8_H358", "technology": "5G", "position": "MID", "brand": "Tecno", "goal": "93%"},
                {"model_name": "KM9_H357", "technology": "5G", "position": "MID", "brand": "Tecno", "goal": "93%"}
            ]
            
            # Add model data to database
            added_count = 0
            for model_data in models_data:
                existing_model = ModelDescription.query.filter_by(model_name=model_data["model_name"]).first()
                if not existing_model:
                    model = ModelDescription(
                        model_name=model_data["model_name"],
                        technology=model_data["technology"],
                        position=model_data["position"],
                        brand=model_data["brand"],
                        goal=model_data["goal"]
                    )
                    db.session.add(model)
                    added_count += 1
                else:
                    print(f"Model {model_data['model_name']} already exists, skipping")
            
            db.session.commit()
            print(f"Successfully imported {added_count} model records to database")
        else:
            print(f"Database already has {model_count} model records, skipping initialization")
        
        # Check project goal data
        project_count = ProjectGoal.query.count()
        print(f"Current project goal count: {project_count}")
        
        if project_count == 0:
            print("Importing project goal data...")
            projects_data = [
                {"project_name": "A666L_F069", "goal": "93%"},
                {"project_name": "P663LN_F069", "goal": "93%"},
                {"project_name": "X6526_V658A", "goal": "93%"},
                {"project_name": "BG7_XE674S", "goal": "93%"},
                {"project_name": "it9020_LS2002", "goal": "NA"},
                {"project_name": "P661N_H334", "goal": "93%"},
                {"project_name": "it2165S_G1808", "goal": "NA"},
                {"project_name": "LI9_H335", "goal": "93%"},
                {"project_name": "X6851_P865A", "goal": "90%"},
                {"project_name": "S667LN_H6933", "goal": "93%"},
                {"project_name": "it2175P_G1808", "goal": "NA"},
                {"project_name": "CL7k_P765A", "goal": "90%"},
                {"project_name": "X6851B_P865A", "goal": "90%"},
                {"project_name": "X6871_H962", "goal": "90%"},
                {"project_name": "CL7_P765A", "goal": "90%"},
                {"project_name": "CL9_H961", "goal": "90%"},
                {"project_name": "X6852_P775A", "goal": "90%"},
                {"project_name": "KJ8_H338", "goal": "93%"},
                {"project_name": "A667LP_SQ373", "goal": "93%"},
                {"project_name": "X6838_P755A", "goal": "93%"},
                {"project_name": "A669L_SQ375", "goal": "93%"},
                {"project_name": "Flip1_MA2432", "goal": "NA"},
                {"project_name": "X6861_H963", "goal": "90%"},
                {"project_name": "KL4_F201", "goal": "93%"},
                {"project_name": "AE10_H833", "goal": "90%"},
                {"project_name": "AE11_H911", "goal": "90%"},
                {"project_name": "X6720_H353", "goal": "93%"},
                {"project_name": "KL8_H353", "goal": "93%"},
                {"project_name": "A671LC_SQ378", "goal": "93%"},
                {"project_name": "X6962_H911", "goal": "90%"},
                {"project_name": "KL8h_H353", "goal": "93%"},
                {"project_name": "KD68CS_KD68CS", "goal": "NA"},
                {"project_name": "KL4H_XE679", "goal": "93%"},
                {"project_name": "IT5032_ET2436", "goal": "NA"},
                {"project_name": "P120_M2001", "goal": "NA"},
                {"project_name": "Ace2p_G1808", "goal": "NA"},
                {"project_name": "It5361_MM61117", "goal": "NA"},
                {"project_name": "It2175P_G1808", "goal": "NA"},
                {"project_name": "P450_MM61120", "goal": "NA"},
                {"project_name": "ACE2L-H_GS1819", "goal": "NA"},
                {"project_name": "It5262_WDS076", "goal": "NA"},
                {"project_name": "It-5095_EY2820", "goal": "NA"},
                {"project_name": "X6532C_MF380", "goal": "93%"},
                {"project_name": "A671N_H353", "goal": "93%"},
                {"project_name": "it3010A_ET1827", "goal": "NA"},
                {"project_name": "BG6m (Export)_F069M", "goal": "93%"},
                {"project_name": "KL5 (Export)_XK678", "goal": "93%"},
                {"project_name": "X6857B_H782", "goal": "90%"},
                {"project_name": "CL7 (Export)Eithopia_P765A", "goal": "90%"},
                {"project_name": "X6870_H781", "goal": "90%"},
                {"project_name": "A6610L_SQ372", "goal": "93%"},
                {"project_name": "It-5608N_G1808", "goal": "NA"},
                {"project_name": "It-9310_LS2801", "goal": "NA"},
                {"project_name": "it2181A_ET1828", "goal": "NA"},
                {"project_name": "A6610L(Export) Latin America_SQ372", "goal": "93%"},
                {"project_name": "LJ8_H781", "goal": "93%"},
                {"project_name": "M3501_M819N", "goal": "93%"},
                {"project_name": "KL5-V_XK678", "goal": "93%"},
                {"project_name": "C671L_SM382", "goal": "93%"},
                {"project_name": "LJ8K_H781", "goal": "93%"},
                {"project_name": "X6525_F069", "goal": "93%"},
                {"project_name": "A663L_V450A", "goal": "93%"},
                {"project_name": "KM4_F151", "goal": "93%"},
                {"project_name": "LJ7_H782", "goal": "93%"},
                {"project_name": "X6726_P526A", "goal": "93%"},
                {"project_name": "V230_GK2819", "goal": "NA"},
                {"project_name": "V220_GY2433", "goal": "NA"},
                {"project_name": "IT9120_SL24B", "goal": "NA"},
                {"project_name": "X6725_F151", "goal": "93%"},
                {"project_name": "X6876_H786", "goal": "90%"},
                {"project_name": "X6730_H358", "goal": "93%"},
                {"project_name": "KM8_H358", "goal": "93%"},
                {"project_name": "KM9_H357", "goal": "93%"}
            ]
            
            # Add project goal data to database
            for project_data in projects_data:
                project = ProjectGoal(
                    project_name=project_data["project_name"],
                    goal=project_data["goal"]
                )
                db.session.add(project)
            
            db.session.commit()
            print(f"Successfully imported {len(projects_data)} project goal records to database")
        else:
            print(f"Database already has {project_count} project goal records, skipping initialization")
        
        print("Database data initialization completed successfully!")
        
    except Exception as e:
        print(f"Database initialization error: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == '__main__':
    init_db()