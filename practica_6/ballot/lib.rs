#![cfg_attr(not(feature = "std"), no_std, no_main)]


#[ink::contract]
pub mod ballot {
    use ink::storage::Mapping;
    use ink::prelude::string::String;
    use ink::prelude::vec::Vec;

    #[derive(Default)]
    #[ink(storage)]
    pub struct Ballot {
        candidates: Mapping<u32, (String, u32)>,
        candidate_count: u32,
        is_open: bool,
        has_voted: Mapping<AccountId, bool>,
    }

    #[ink(event)]
    pub struct Voted {
        #[ink(topic)]
        by: AccountId,
        candidate: String,
    }

    impl Ballot {
        #[ink(constructor)]
        pub fn new(candidate_names: Vec<String>) -> Self {
            let mut candidates = Mapping::default();
            let candidate_count: u32 = candidate_names.len().try_into().expect("Too many candidates");
            for (i, name) in candidate_names.into_iter().enumerate() {
                let index: u32 = i.try_into().expect("Index out of bounds");
                candidates.insert(index, &(name, 0));
            }
            Self {
                candidates,
                candidate_count,
                is_open: true,
                has_voted: Mapping::default(),
            }
        }

        #[ink(message)]
        pub fn vote(&mut self, candidate_index: u32) {
            assert!(self.is_open, "Voting is closed");
            assert!(candidate_index < self.candidate_count, "Invalid candidate index");
            assert!(!self.has_voted.get(&self.env().caller()).unwrap_or_default(), "You have already voted");

            let mut candidate = self.candidates.get(candidate_index).unwrap();
            candidate.1 = candidate.1.checked_add(1).expect("Vote count overflow");
            self.candidates.insert(candidate_index, &candidate);
            self.has_voted.insert(self.env().caller(), &true);

            self.env().emit_event(Voted {
                by: self.env().caller(),
                candidate: candidate.0.clone(),
            });
        }

        #[ink(message)]
        pub fn close_ballot(&mut self) {
            self.is_open = false;
        }

        #[ink(message)]
        pub fn get_winner(&self) -> String {
            let mut winning_vote_count = 0;
            let mut winning_candidate = String::new();
            for i in 0..self.candidate_count {
                let candidate = self.candidates.get(i).unwrap();
                if candidate.1 > winning_vote_count {
                    winning_vote_count = candidate.1;
                    winning_candidate = candidate.0.clone();
                }
            }
            winning_candidate
        }

        #[ink(message)]
        pub fn get_candidate_count(&self) -> u32 {
            self.candidate_count
        }
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[ink::test]
        fn test_voting_process() {
            let candidate_names = vec!["Alice".to_string(), "Bob".to_string()];
            let mut contract = Ballot::new(candidate_names);
            assert_eq!(contract.get_candidate_count(), 2);

            contract.vote(0);
            assert_eq!(contract.get_winner(), "Alice");

            contract.close_ballot();
            assert!(contract.is_open == false);
        }
    }
}
